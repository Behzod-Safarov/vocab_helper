"""
Learn Command Handler
Handles /learn command and learning functionality
"""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.exceptions import TelegramBadRequest

from storage.json_storage import UserDataManager, get_unit_words
from modules.vocabulary import VocabularyManager, format_word_for_display, format_word_card
from keyboards.inline import (
    get_learn_menu_keyboard,
    get_level_selection_keyboard,
    get_unit_selection_keyboard,
    get_word_learning_keyboard,
    get_flashcard_keyboard,
    get_flashcard_response_keyboard,
    get_add_word_keyboard,
    get_back_button,
)
from utils.helpers import get_random_motivation, get_random_encouragement, create_word_id
from locales import get_text
import config

router = Router()


class AddWordStates(StatesGroup):
    """States for adding custom words"""
    waiting_for_word = State()
    waiting_for_meaning = State()
    waiting_for_example = State()
    waiting_for_synonyms = State()


class LearnSessionStates(StatesGroup):
    """States for learning session"""
    learning = State()


async def get_user_settings(user_id: int) -> tuple:
    """Get user's language and translation settings"""
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    settings = user_manager.data.get("settings", {})
    lang = settings.get("language", "en")
    trans_lang = settings.get("translation_language", "both")
    return lang, trans_lang


@router.message(Command("learn"))
async def cmd_learn(message: Message):
    """Handle /learn command"""
    user_id = message.from_user.id
    lang, _ = await get_user_settings(user_id)
    
    await message.answer(
        get_text("learn_menu_title", lang),
        parse_mode="Markdown",
        reply_markup=get_learn_menu_keyboard(lang)
    )


@router.callback_query(F.data == "menu:learn")
async def show_learn_menu(callback: CallbackQuery):
    """Show learning menu"""
    user_id = callback.from_user.id
    lang, _ = await get_user_settings(user_id)
    
    await callback.message.edit_text(
        get_text("learn_menu_title", lang),
        parse_mode="Markdown",
        reply_markup=get_learn_menu_keyboard(lang)
    )
    await callback.answer()


@router.callback_query(F.data == "learn:menu")
async def back_to_learn_menu(callback: CallbackQuery, state: FSMContext):
    """Back to learn menu"""
    await state.clear()
    user_id = callback.from_user.id
    lang, _ = await get_user_settings(user_id)
    
    await callback.message.edit_text(
        get_text("learn_menu_title", lang),
        parse_mode="Markdown",
        reply_markup=get_learn_menu_keyboard(lang)
    )
    await callback.answer()


# ============ 4000 Words Learning ============

@router.callback_query(F.data == "learn:4000")
async def learn_4000_select_level(callback: CallbackQuery):
    """Select level for learning"""
    user_id = callback.from_user.id
    lang, _ = await get_user_settings(user_id)
    
    await callback.message.edit_text(
        get_text("select_level", lang),
        parse_mode="Markdown",
        reply_markup=get_level_selection_keyboard("learn", lang)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("learn:level:"))
async def learn_select_unit(callback: CallbackQuery):
    """Select unit for learning"""
    parts = callback.data.split(":")
    level = int(parts[2])
    page = int(parts[4]) if len(parts) > 4 and parts[3] == "page" else 0
    
    user_id = callback.from_user.id
    lang, _ = await get_user_settings(user_id)
    
    vocab_manager = VocabularyManager(user_id)
    await vocab_manager.initialize()
    
    # Get level progress
    progress = await vocab_manager.get_user_progress_for_level(level)
    
    await callback.message.edit_text(
        get_text("level_progress", lang, 
                 level=level, 
                 rate=progress['completion_rate'],
                 learned=progress['learned'],
                 total=progress['total_words']),
        parse_mode="Markdown",
        reply_markup=get_unit_selection_keyboard(level, "learn", page, lang=lang)
    )
    await callback.answer()


@router.callback_query(F.data.regexp(r"^learn:L(\d+)U(\d+)$"))
async def start_learning_unit(callback: CallbackQuery, state: FSMContext):
    """Start learning words from a unit"""
    import re
    match = re.match(r"^learn:L(\d+)U(\d+)$", callback.data)
    level = int(match.group(1))
    unit = int(match.group(2))
    
    user_id = callback.from_user.id
    lang, trans_lang = await get_user_settings(user_id)
    
    # Get words from the unit
    words = await get_unit_words(level, unit)
    
    if not words:
        await callback.message.edit_text(
            get_text("error_no_words", lang, level=level, unit=unit),
            reply_markup=get_back_button("learn:4000", lang)
        )
        await callback.answer()
        return
    
    # Initialize learning session
    vocab_manager = VocabularyManager(user_id)
    await vocab_manager.initialize()
    
    # Find first new/unlearned word
    word_status = vocab_manager.user_manager.data["words_4000_progress"]["word_status"]
    
    current_word_idx = 0
    for i, word in enumerate(words):
        word_id = create_word_id(level, unit, i)
        status = word_status.get(word_id, {}).get("status", "new")
        if status in ["new", "learning", "weak"]:
            current_word_idx = i
            break
    
    # Store session state
    await state.set_state(LearnSessionStates.learning)
    await state.update_data(
        level=level,
        unit=unit,
        current_idx=current_word_idx,
        total_words=len(words)
    )
    
    # Show first word
    word = words[current_word_idx]
    word["level"] = level
    word["unit"] = unit
    word_id = create_word_id(level, unit, current_word_idx)
    
    await callback.message.edit_text(
        get_text("word_counter", lang, level=level, unit=unit, current=current_word_idx + 1, total=len(words)) + "\n\n" +
        format_word_for_display(word, show_answer=True, lang=lang, translation_lang=trans_lang),
        parse_mode="Markdown",
        reply_markup=get_word_learning_keyboard(word_id, lang)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("learn:know:"))
async def word_known(callback: CallbackQuery, state: FSMContext):
    """User knows the word"""
    word_id = callback.data.split(":")[-1]
    user_id = callback.from_user.id
    
    # Update word status
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    await user_manager.update_word_status(word_id, is_4000=True, correct=True)
    await user_manager.update_stats(correct=True)
    
    # Show next word
    await show_next_learning_word(callback, state)


@router.callback_query(F.data.startswith("learn:unknown:"))
async def word_unknown(callback: CallbackQuery, state: FSMContext):
    """User doesn't know the word"""
    word_id = callback.data.split(":")[-1]
    user_id = callback.from_user.id
    
    # Update word status
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    await user_manager.update_word_status(word_id, is_4000=True, correct=False)
    await user_manager.update_stats(correct=False)
    
    lang, _ = await get_user_settings(user_id)
    await callback.answer(get_random_encouragement(lang))
    
    # Show next word
    await show_next_learning_word(callback, state)


@router.callback_query(F.data.startswith("learn:next:"))
async def next_word(callback: CallbackQuery, state: FSMContext):
    """Skip to next word"""
    await show_next_learning_word(callback, state)


async def show_next_learning_word(callback: CallbackQuery, state: FSMContext):
    """Show the next word in learning session"""
    user_id = callback.from_user.id
    lang, trans_lang = await get_user_settings(user_id)
    
    data = await state.get_data()
    
    # Delete previous audio message if exists
    prev_audio_id = data.get("last_audio_message_id") if data else None
    if prev_audio_id:
        try:
            await callback.bot.delete_message(
                chat_id=callback.message.chat.id,
                message_id=prev_audio_id
            )
        except Exception:
            pass  # Ignore if message already deleted
        await state.update_data(last_audio_message_id=None)
    
    # Check if we have valid learning session data
    if not data or "level" not in data or "unit" not in data:
        await callback.message.edit_text(
            get_text("session_expired", lang),
            reply_markup=get_back_button("learn:4000", lang)
        )
        await callback.answer()
        return
    
    level = data["level"]
    unit = data["unit"]
    current_idx = data.get("current_idx", 0) + 1
    total_words = data.get("total_words", 0)
    
    if current_idx >= total_words:
        # Unit completed
        await state.clear()
        await callback.message.edit_text(
            get_text("unit_complete", lang, unit=unit, level=level) + f"\n\n{get_random_motivation(lang)}",
            parse_mode="Markdown",
            reply_markup=get_back_button("learn:4000", lang)
        )
        await callback.answer("🎉")
        return
    
    # Get next word
    words = await get_unit_words(level, unit)
    word = words[current_idx]
    word["level"] = level
    word["unit"] = unit
    word_id = create_word_id(level, unit, current_idx)
    
    # Update state
    await state.update_data(current_idx=current_idx)
    
    await callback.message.edit_text(
        get_text("word_progress", lang, level=level, unit=unit, current=current_idx + 1, total=total_words) + "\n\n" +
        format_word_for_display(word, show_answer=True, lang=lang, translation_lang=trans_lang),
        parse_mode="Markdown",
        reply_markup=get_word_learning_keyboard(word_id, lang)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("learn:example:"))
async def show_example(callback: CallbackQuery):
    """Show word example"""
    user_id = callback.from_user.id
    lang, trans_lang = await get_user_settings(user_id)
    
    word_id = callback.data.split(":")[-1]
    
    # Parse word ID
    from utils.helpers import parse_word_id
    parsed = parse_word_id(word_id)
    
    if parsed:
        words = await get_unit_words(parsed["level"], parsed["unit"])
        if words and parsed["word_index"] < len(words):
            word = words[parsed["word_index"]]
            example = word.get("example", get_text("no_example", lang))
            await callback.answer(f"📝 {example}", show_alert=True)
            return
    
    await callback.answer(get_text("example_not_available", lang), show_alert=True)


@router.callback_query(F.data.startswith("learn:audio:"))
async def play_pronunciation(callback: CallbackQuery, state: FSMContext):
    """Play word pronunciation using TTS"""
    from aiogram.types import FSInputFile
    import tempfile
    import os
    
    user_id = callback.from_user.id
    lang, trans_lang = await get_user_settings(user_id)
    
    word_id = callback.data.split(":")[-1]
    
    # Parse word ID to get the word
    from utils.helpers import parse_word_id
    parsed = parse_word_id(word_id)
    
    word_text = None
    
    if parsed:
        words = await get_unit_words(parsed["level"], parsed["unit"])
        if words and parsed["word_index"] < len(words):
            word_text = words[parsed["word_index"]].get("word", "")
    else:
        # Custom word - try to get from user's custom vocabulary
        user_manager = UserDataManager(user_id)
        await user_manager.load()
        custom_words = user_manager.data.get("custom_vocabulary", [])
        for cw in custom_words:
            if cw.get("id") == word_id:
                word_text = cw.get("word", "")
                break
    
    if not word_text:
        await callback.answer(get_text("pronunciation_not_available", lang), show_alert=True)
        return
    
    try:
        from gtts import gTTS
        
        # Create TTS audio
        tts = gTTS(text=word_text, lang='en', slow=False)
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
            tmp_path = tmp_file.name
            tts.save(tmp_path)
        
        # Send voice message
        audio_file = FSInputFile(tmp_path, filename=f"{word_text}.mp3")
        voice_msg = await callback.message.answer_voice(
            audio_file,
            caption=f"🔊 *{word_text}*",
            parse_mode="Markdown"
        )
        
        # Store audio message ID for later deletion
        data = await state.get_data()
        prev_audio_id = data.get("last_audio_message_id")
        
        # Delete previous audio if exists
        if prev_audio_id:
            try:
                await callback.bot.delete_message(
                    chat_id=callback.message.chat.id,
                    message_id=prev_audio_id
                )
            except Exception:
                pass  # Ignore if message already deleted
        
        # Save new audio message ID
        await state.update_data(last_audio_message_id=voice_msg.message_id)
        
        # Clean up temp file
        os.unlink(tmp_path)
        
        await callback.answer()
        
    except ImportError:
        await callback.answer(
            get_text("tts_not_installed", lang),
            show_alert=True
        )
    except Exception as e:
        await callback.answer(
            get_text("pronunciation_error", lang),
            show_alert=True
        )


# ============ Custom Words ============

@router.callback_query(F.data == "learn:custom")
async def show_custom_words(callback: CallbackQuery):
    """Show custom vocabulary"""
    user_id = callback.from_user.id
    lang, trans_lang = await get_user_settings(user_id)
    
    vocab_manager = VocabularyManager(user_id)
    await vocab_manager.initialize()
    
    words = await vocab_manager.get_custom_words()
    
    try:
        if not words:
            await callback.message.edit_text(
                get_text("custom_words_empty", lang),
                parse_mode="Markdown",
                reply_markup=get_learn_menu_keyboard(lang)
            )
        else:
            word_list = "\n".join([f"• {w['word']}" for w in words[:10]])
            await callback.message.edit_text(
                get_text("custom_words_list", lang, count=len(words), word_list=word_list, more="..." if len(words) > 10 else ""),
                parse_mode="Markdown",
                reply_markup=get_learn_menu_keyboard(lang)
            )
    except TelegramBadRequest as e:
        if "message is not modified" not in str(e):
            raise
    
    await callback.answer()


@router.callback_query(F.data == "learn:add")
async def start_add_word(callback: CallbackQuery, state: FSMContext):
    """Start adding a new word"""
    user_id = callback.from_user.id
    lang, trans_lang = await get_user_settings(user_id)
    
    await state.set_state(AddWordStates.waiting_for_word)
    
    await callback.message.edit_text(
        get_text("add_word_prompt", lang),
        parse_mode="Markdown",
        reply_markup=get_add_word_keyboard(lang)
    )
    await callback.answer()


@router.message(AddWordStates.waiting_for_word)
async def receive_word(message: Message, state: FSMContext):
    """Receive the word to add"""
    user_id = message.from_user.id
    lang, trans_lang = await get_user_settings(user_id)
    
    from utils.helpers import validate_word_input
    
    word = message.text.strip()
    is_valid, error = validate_word_input(word, lang)
    
    if not is_valid:
        await message.answer(
            f"❌ {error}\n\n{get_text('try_again', lang)}",
            reply_markup=get_add_word_keyboard(lang)
        )
        return
    
    await state.update_data(word=word)
    await state.set_state(AddWordStates.waiting_for_meaning)
    
    await message.answer(
        get_text("add_word_meaning_prompt", lang, word=word),
        parse_mode="Markdown",
        reply_markup=get_add_word_keyboard(lang)
    )


@router.message(AddWordStates.waiting_for_meaning)
async def receive_meaning(message: Message, state: FSMContext):
    """Receive the word meaning"""
    user_id = message.from_user.id
    lang, trans_lang = await get_user_settings(user_id)
    
    from utils.helpers import validate_meaning_input
    
    meaning = message.text.strip()
    is_valid, error = validate_meaning_input(meaning, lang)
    
    if not is_valid:
        await message.answer(
            f"❌ {error}\n\n{get_text('try_again', lang)}",
            reply_markup=get_add_word_keyboard(lang)
        )
        return
    
    await state.update_data(meaning=meaning)
    await state.set_state(AddWordStates.waiting_for_example)
    
    await message.answer(
        get_text("add_word_example_prompt", lang),
        reply_markup=get_add_word_keyboard(lang)
    )


@router.message(AddWordStates.waiting_for_example)
async def receive_example(message: Message, state: FSMContext):
    """Receive example sentence"""
    user_id = message.from_user.id
    lang, trans_lang = await get_user_settings(user_id)
    
    example = None if message.text.strip() == "/skip" else message.text.strip()
    
    await state.update_data(example=example)
    
    # Save the word
    data = await state.get_data()
    
    vocab_manager = VocabularyManager(user_id)
    await vocab_manager.initialize()
    
    await vocab_manager.add_custom_word(
        word=data["word"],
        meaning=data["meaning"],
        example=example
    )
    
    await state.clear()
    
    await message.answer(
        get_text("word_added_success", lang, word=data['word'], meaning=data['meaning'], example=example or get_text("not_provided", lang)) + f"\n\n{get_random_motivation(lang)}",
        parse_mode="Markdown",
        reply_markup=get_learn_menu_keyboard(lang)
    )


# ============ Review Due Words ============

@router.callback_query(F.data == "learn:review")
async def start_review(callback: CallbackQuery, state: FSMContext):
    """Start review of due words"""
    user_id = callback.from_user.id
    lang, trans_lang = await get_user_settings(user_id)
    
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    
    due_words = await user_manager.get_words_due_for_review()
    
    if not due_words:
        try:
            await callback.message.edit_text(
                get_text("review_all_caught_up", lang),
                parse_mode="Markdown",
                reply_markup=get_learn_menu_keyboard(lang)
            )
        except TelegramBadRequest as e:
            if "message is not modified" not in str(e):
                raise
        await callback.answer()
        return
    
    # Store review session
    await state.set_state(LearnSessionStates.learning)
    await state.update_data(
        review_mode=True,
        due_words=[w["word_id"] for w in due_words],
        current_review_idx=0
    )
    
    # Show first word as flashcard
    first_word = due_words[0]
    word_id = first_word["word_id"]
    
    # Get word data
    if first_word["is_4000"]:
        from utils.helpers import parse_word_id
        parsed = parse_word_id(word_id)
        if parsed:
            words = await get_unit_words(parsed["level"], parsed["unit"])
            if words and parsed["word_index"] < len(words):
                word = words[parsed["word_index"]]
                word["level"] = parsed["level"]
                word["unit"] = parsed["unit"]
                
                await callback.message.edit_text(
                    get_text("review_progress", lang, current=1, total=len(due_words)) + "\n\n" +
                    format_word_card(word, lang),
                    parse_mode="Markdown",
                    reply_markup=get_flashcard_keyboard(word_id, lang)
                )
                await callback.answer()
                return
    else:
        # Handle custom words
        word_data = first_word.get("word_data")
        if word_data:
            # Format custom word for display
            custom_word = {
                "word": word_data.get("word", ""),
                "meaning": word_data.get("meaning", ""),
                "example": word_data.get("example", ""),
                "definition": word_data.get("meaning", ""),
            }
            
            await callback.message.edit_text(
                get_text("review_progress", lang, current=1, total=len(due_words)) + "\n\n" +
                format_word_card(custom_word, lang),
                parse_mode="Markdown",
                reply_markup=get_flashcard_keyboard(word_id, lang)
            )
            await callback.answer()
            return
    
    await callback.answer(get_text("error_loading_word", lang))


@router.callback_query(F.data.startswith("flash:show:"))
async def show_flashcard_answer(callback: CallbackQuery, state: FSMContext):
    """Show the answer for a flashcard"""
    user_id = callback.from_user.id
    lang, trans_lang = await get_user_settings(user_id)
    
    word_id = callback.data.split(":")[-1]
    
    from utils.helpers import parse_word_id
    parsed = parse_word_id(word_id)
    
    data = await state.get_data()
    due_words = data.get("due_words", [])
    current_idx = data.get("current_review_idx", 0)
    
    if parsed:
        # 4000 word
        words = await get_unit_words(parsed["level"], parsed["unit"])
        if words and parsed["word_index"] < len(words):
            word = words[parsed["word_index"]]
            word["level"] = parsed["level"]
            word["unit"] = parsed["unit"]
            
            await callback.message.edit_text(
                get_text("review_progress", lang, current=current_idx + 1, total=len(due_words)) + "\n\n" +
                format_word_for_display(word, show_answer=True, lang=lang, translation_lang=trans_lang),
                parse_mode="Markdown",
                reply_markup=get_flashcard_response_keyboard(word_id, lang)
            )
            await callback.answer()
            return
    elif word_id.startswith("custom_"):
        # Custom word
        user_manager = UserDataManager(user_id)
        await user_manager.load()
        custom_words = user_manager.data.get("custom_vocabulary", [])
        for cw in custom_words:
            if cw.get("id") == word_id:
                word = {
                    "word": cw.get("word", ""),
                    "definition": cw.get("meaning", ""),
                    "example": cw.get("example", ""),
                    "meaning": cw.get("meaning", ""),
                }
                await callback.message.edit_text(
                    get_text("review_progress", lang, current=current_idx + 1, total=len(due_words)) + "\n\n" +
                    format_word_for_display(word, show_answer=True, lang=lang, translation_lang=trans_lang),
                    parse_mode="Markdown",
                    reply_markup=get_flashcard_response_keyboard(word_id, lang)
                )
                await callback.answer()
                return
    
    await callback.answer(get_text("error_showing_answer", lang))


@router.callback_query(F.data.startswith("flash:correct:"))
async def flashcard_correct(callback: CallbackQuery, state: FSMContext):
    """User remembered the word"""
    user_id = callback.from_user.id
    lang, trans_lang = await get_user_settings(user_id)
    
    word_id = callback.data.split(":")[-1]
    is_4000 = not word_id.startswith("custom_")
    
    # Update word status
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    await user_manager.update_word_status(word_id, is_4000=is_4000, correct=True)
    await user_manager.update_stats(correct=True)
    
    await callback.answer(get_text("great_job", lang))
    
    # Show next review word
    await show_next_review_word(callback, state, lang, trans_lang)


@router.callback_query(F.data.startswith("flash:wrong:"))
async def flashcard_wrong(callback: CallbackQuery, state: FSMContext):
    """User forgot the word"""
    user_id = callback.from_user.id
    lang, trans_lang = await get_user_settings(user_id)
    
    word_id = callback.data.split(":")[-1]
    is_4000 = not word_id.startswith("custom_")
    
    # Update word status
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    await user_manager.update_word_status(word_id, is_4000=is_4000, correct=False)
    await user_manager.update_stats(correct=False)
    
    await callback.answer(get_random_encouragement(lang))
    
    # Show next review word
    await show_next_review_word(callback, state, lang, trans_lang)


async def show_next_review_word(callback: CallbackQuery, state: FSMContext, lang: str = "en", trans_lang: str = "both"):
    """Show the next word in review session"""
    data = await state.get_data()
    
    if not data or not data.get("review_mode"):
        await callback.message.edit_text(
            get_text("session_expired", lang),
            reply_markup=get_learn_menu_keyboard(lang)
        )
        return
    
    due_words = data.get("due_words", [])
    current_idx = data.get("current_review_idx", 0) + 1
    
    if current_idx >= len(due_words):
        # Review completed
        await state.clear()
        await callback.message.edit_text(
            get_text("review_complete", lang, count=len(due_words)) + f"\n\n{get_random_motivation(lang)}",
            parse_mode="Markdown",
            reply_markup=get_learn_menu_keyboard(lang)
        )
        return
    
    # Update state
    await state.update_data(current_review_idx=current_idx)
    
    # Get next word
    word_id = due_words[current_idx]
    
    from utils.helpers import parse_word_id
    parsed = parse_word_id(word_id)
    
    if parsed:
        # 4000 word
        words = await get_unit_words(parsed["level"], parsed["unit"])
        if words and parsed["word_index"] < len(words):
            word = words[parsed["word_index"]]
            word["level"] = parsed["level"]
            word["unit"] = parsed["unit"]
            
            await callback.message.edit_text(
                get_text("review_progress", lang, current=current_idx + 1, total=len(due_words)) + "\n\n" +
                format_word_card(word, lang),
                parse_mode="Markdown",
                reply_markup=get_flashcard_keyboard(word_id, lang)
            )
            return
    elif word_id.startswith("custom_"):
        # Custom word
        user_id = callback.from_user.id
        user_manager = UserDataManager(user_id)
        await user_manager.load()
        custom_words = user_manager.data.get("custom_vocabulary", [])
        for cw in custom_words:
            if cw.get("id") == word_id:
                word = {
                    "word": cw.get("word", ""),
                    "definition": cw.get("meaning", ""),
                    "example": cw.get("example", ""),
                    "meaning": cw.get("meaning", ""),
                }
                await callback.message.edit_text(
                    get_text("review_progress", lang, current=current_idx + 1, total=len(due_words)) + "\n\n" +
                    format_word_card(word, lang),
                    parse_mode="Markdown",
                    reply_markup=get_flashcard_keyboard(word_id, lang)
                )
                return
    
    # Error case - skip to next
    await show_next_review_word(callback, state, lang, trans_lang)
