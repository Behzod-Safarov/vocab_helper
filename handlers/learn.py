"""
Learn Command Handler
Handles /learn command and learning functionality
"""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

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


@router.message(Command("learn"))
async def cmd_learn(message: Message):
    """Handle /learn command"""
    await message.answer(
        "📚 *Learning Mode*\n\nChoose what you'd like to learn:",
        parse_mode="Markdown",
        reply_markup=get_learn_menu_keyboard()
    )


@router.callback_query(F.data == "menu:learn")
async def show_learn_menu(callback: CallbackQuery):
    """Show learning menu"""
    await callback.message.edit_text(
        "📚 *Learning Mode*\n\nChoose what you'd like to learn:",
        parse_mode="Markdown",
        reply_markup=get_learn_menu_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "learn:menu")
async def back_to_learn_menu(callback: CallbackQuery, state: FSMContext):
    """Back to learn menu"""
    await state.clear()
    await callback.message.edit_text(
        "📚 *Learning Mode*\n\nChoose what you'd like to learn:",
        parse_mode="Markdown",
        reply_markup=get_learn_menu_keyboard()
    )
    await callback.answer()


# ============ 4000 Words Learning ============

@router.callback_query(F.data == "learn:4000")
async def learn_4000_select_level(callback: CallbackQuery):
    """Select level for learning"""
    await callback.message.edit_text(
        "📘 *4000 Essential English Words*\n\nSelect a level to learn:",
        parse_mode="Markdown",
        reply_markup=get_level_selection_keyboard("learn")
    )
    await callback.answer()


@router.callback_query(F.data.startswith("learn:level:"))
async def learn_select_unit(callback: CallbackQuery):
    """Select unit for learning"""
    parts = callback.data.split(":")
    level = int(parts[2])
    page = int(parts[4]) if len(parts) > 4 and parts[3] == "page" else 0
    
    user_id = callback.from_user.id
    vocab_manager = VocabularyManager(user_id)
    await vocab_manager.initialize()
    
    # Get level progress
    progress = await vocab_manager.get_user_progress_for_level(level)
    
    await callback.message.edit_text(
        f"📘 *Level {level}*\n\n"
        f"📊 Progress: {progress['completion_rate']:.1f}%\n"
        f"✅ Learned: {progress['learned']}/{progress['total_words']}\n\n"
        f"Select a unit:",
        parse_mode="Markdown",
        reply_markup=get_unit_selection_keyboard(level, "learn", page)
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
    
    # Get words from the unit
    words = await get_unit_words(level, unit)
    
    if not words:
        await callback.message.edit_text(
            f"❌ No words found for Level {level} Unit {unit}.\n\n"
            "Please check if the word data is available.",
            reply_markup=get_back_button("learn:4000")
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
        f"📖 *Level {level} • Unit {unit}* (Word {current_word_idx + 1}/{len(words)})\n\n" +
        format_word_for_display(word, show_answer=True),
        parse_mode="Markdown",
        reply_markup=get_word_learning_keyboard(word_id)
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
    
    await callback.answer(get_random_encouragement())
    
    # Show next word
    await show_next_learning_word(callback, state)


@router.callback_query(F.data.startswith("learn:next:"))
async def next_word(callback: CallbackQuery, state: FSMContext):
    """Skip to next word"""
    await show_next_learning_word(callback, state)


async def show_next_learning_word(callback: CallbackQuery, state: FSMContext):
    """Show the next word in learning session"""
    data = await state.get_data()
    
    if not data:
        await callback.message.edit_text(
            "Session expired. Please start a new learning session.",
            reply_markup=get_back_button("learn:4000")
        )
        await callback.answer()
        return
    
    level = data["level"]
    unit = data["unit"]
    current_idx = data["current_idx"] + 1
    total_words = data["total_words"]
    
    if current_idx >= total_words:
        # Unit completed
        await state.clear()
        await callback.message.edit_text(
            f"🎉 *Congratulations!*\n\n"
            f"You've completed Level {level} Unit {unit}!\n\n"
            f"{get_random_motivation()}",
            parse_mode="Markdown",
            reply_markup=get_back_button("learn:4000")
        )
        await callback.answer("Unit completed! 🎉")
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
        f"📖 *Level {level} • Unit {unit}* (Word {current_idx + 1}/{total_words})\n\n" +
        format_word_for_display(word, show_answer=True),
        parse_mode="Markdown",
        reply_markup=get_word_learning_keyboard(word_id)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("learn:example:"))
async def show_example(callback: CallbackQuery):
    """Show word example"""
    word_id = callback.data.split(":")[-1]
    
    # Parse word ID
    from utils.helpers import parse_word_id
    parsed = parse_word_id(word_id)
    
    if parsed:
        words = await get_unit_words(parsed["level"], parsed["unit"])
        if words and parsed["word_index"] < len(words):
            word = words[parsed["word_index"]]
            example = word.get("example", "No example available.")
            await callback.answer(f"📝 {example}", show_alert=True)
            return
    
    await callback.answer("Example not available", show_alert=True)


# ============ Custom Words ============

@router.callback_query(F.data == "learn:custom")
async def show_custom_words(callback: CallbackQuery):
    """Show custom vocabulary"""
    user_id = callback.from_user.id
    vocab_manager = VocabularyManager(user_id)
    await vocab_manager.initialize()
    
    words = await vocab_manager.get_custom_words()
    
    if not words:
        await callback.message.edit_text(
            "✏️ *My Custom Words*\n\n"
            "You haven't added any custom words yet.\n\n"
            "Tap 'Add New Word' to start building your vocabulary!",
            parse_mode="Markdown",
            reply_markup=get_learn_menu_keyboard()
        )
    else:
        word_list = "\n".join([f"• {w['word']}" for w in words[:10]])
        await callback.message.edit_text(
            f"✏️ *My Custom Words* ({len(words)} words)\n\n"
            f"{word_list}\n"
            f"{'...' if len(words) > 10 else ''}",
            parse_mode="Markdown",
            reply_markup=get_learn_menu_keyboard()
        )
    
    await callback.answer()


@router.callback_query(F.data == "learn:add")
async def start_add_word(callback: CallbackQuery, state: FSMContext):
    """Start adding a new word"""
    await state.set_state(AddWordStates.waiting_for_word)
    
    await callback.message.edit_text(
        "➕ *Add New Word*\n\n"
        "Please send me the word you want to add:",
        parse_mode="Markdown",
        reply_markup=get_add_word_keyboard()
    )
    await callback.answer()


@router.message(AddWordStates.waiting_for_word)
async def receive_word(message: Message, state: FSMContext):
    """Receive the word to add"""
    from utils.helpers import validate_word_input
    
    word = message.text.strip()
    is_valid, error = validate_word_input(word)
    
    if not is_valid:
        await message.answer(
            f"❌ {error}\n\nPlease try again:",
            reply_markup=get_add_word_keyboard()
        )
        return
    
    await state.update_data(word=word)
    await state.set_state(AddWordStates.waiting_for_meaning)
    
    await message.answer(
        f"✅ Word: *{word}*\n\n"
        "Now send me the meaning/definition:",
        parse_mode="Markdown",
        reply_markup=get_add_word_keyboard()
    )


@router.message(AddWordStates.waiting_for_meaning)
async def receive_meaning(message: Message, state: FSMContext):
    """Receive the word meaning"""
    from utils.helpers import validate_meaning_input
    
    meaning = message.text.strip()
    is_valid, error = validate_meaning_input(meaning)
    
    if not is_valid:
        await message.answer(
            f"❌ {error}\n\nPlease try again:",
            reply_markup=get_add_word_keyboard()
        )
        return
    
    await state.update_data(meaning=meaning)
    await state.set_state(AddWordStates.waiting_for_example)
    
    await message.answer(
        "📝 Great! Now send an example sentence.\n\n"
        "(Or send /skip to skip this step)",
        reply_markup=get_add_word_keyboard()
    )


@router.message(AddWordStates.waiting_for_example)
async def receive_example(message: Message, state: FSMContext):
    """Receive example sentence"""
    example = None if message.text.strip() == "/skip" else message.text.strip()
    
    await state.update_data(example=example)
    
    # Save the word
    user_id = message.from_user.id
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
        f"✅ *Word Added Successfully!*\n\n"
        f"📚 Word: *{data['word']}*\n"
        f"📖 Meaning: {data['meaning']}\n"
        f"💬 Example: {example or 'Not provided'}\n\n"
        f"{get_random_motivation()}",
        parse_mode="Markdown",
        reply_markup=get_learn_menu_keyboard()
    )


# ============ Review Due Words ============

@router.callback_query(F.data == "learn:review")
async def start_review(callback: CallbackQuery, state: FSMContext):
    """Start review of due words"""
    user_id = callback.from_user.id
    
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    
    due_words = await user_manager.get_words_due_for_review()
    
    if not due_words:
        await callback.message.edit_text(
            "✨ *All caught up!*\n\n"
            "You don't have any words due for review right now.\n"
            "Keep learning new words or check back later!",
            parse_mode="Markdown",
            reply_markup=get_learn_menu_keyboard()
        )
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
                    f"🔄 *Review* (1/{len(due_words)})\n\n" +
                    format_word_card(word),
                    parse_mode="Markdown",
                    reply_markup=get_flashcard_keyboard(word_id)
                )
                await callback.answer()
                return
    
    await callback.answer("Error loading word")


@router.callback_query(F.data.startswith("flash:show:"))
async def show_flashcard_answer(callback: CallbackQuery, state: FSMContext):
    """Show the answer for a flashcard"""
    word_id = callback.data.split(":")[-1]
    
    from utils.helpers import parse_word_id
    parsed = parse_word_id(word_id)
    
    if parsed:
        words = await get_unit_words(parsed["level"], parsed["unit"])
        if words and parsed["word_index"] < len(words):
            word = words[parsed["word_index"]]
            word["level"] = parsed["level"]
            word["unit"] = parsed["unit"]
            
            data = await state.get_data()
            due_words = data.get("due_words", [])
            current_idx = data.get("current_review_idx", 0)
            
            await callback.message.edit_text(
                f"🔄 *Review* ({current_idx + 1}/{len(due_words)})\n\n" +
                format_word_for_display(word, show_answer=True),
                parse_mode="Markdown",
                reply_markup=get_flashcard_response_keyboard(word_id)
            )
            await callback.answer()
            return
    
    await callback.answer("Error showing answer")


@router.callback_query(F.data.startswith("flash:correct:"))
async def flashcard_correct(callback: CallbackQuery, state: FSMContext):
    """User remembered the word"""
    word_id = callback.data.split(":")[-1]
    user_id = callback.from_user.id
    
    # Update word status
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    await user_manager.update_word_status(word_id, is_4000=True, correct=True)
    await user_manager.update_stats(correct=True)
    
    await callback.answer("✅ Great job!")
    
    # Show next review word
    await show_next_review_word(callback, state)


@router.callback_query(F.data.startswith("flash:wrong:"))
async def flashcard_wrong(callback: CallbackQuery, state: FSMContext):
    """User forgot the word"""
    word_id = callback.data.split(":")[-1]
    user_id = callback.from_user.id
    
    # Update word status
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    await user_manager.update_word_status(word_id, is_4000=True, correct=False)
    await user_manager.update_stats(correct=False)
    
    await callback.answer(get_random_encouragement())
    
    # Show next review word
    await show_next_review_word(callback, state)


async def show_next_review_word(callback: CallbackQuery, state: FSMContext):
    """Show the next word in review session"""
    data = await state.get_data()
    
    if not data or not data.get("review_mode"):
        await callback.message.edit_text(
            "Session expired. Please start a new review session.",
            reply_markup=get_learn_menu_keyboard()
        )
        return
    
    due_words = data.get("due_words", [])
    current_idx = data.get("current_review_idx", 0) + 1
    
    if current_idx >= len(due_words):
        # Review completed
        await state.clear()
        await callback.message.edit_text(
            f"🎉 *Review Complete!*\n\n"
            f"You reviewed {len(due_words)} words.\n\n"
            f"{get_random_motivation()}",
            parse_mode="Markdown",
            reply_markup=get_learn_menu_keyboard()
        )
        return
    
    # Update state
    await state.update_data(current_review_idx=current_idx)
    
    # Get next word
    word_id = due_words[current_idx]
    
    from utils.helpers import parse_word_id
    parsed = parse_word_id(word_id)
    
    if parsed:
        words = await get_unit_words(parsed["level"], parsed["unit"])
        if words and parsed["word_index"] < len(words):
            word = words[parsed["word_index"]]
            word["level"] = parsed["level"]
            word["unit"] = parsed["unit"]
            
            await callback.message.edit_text(
                f"🔄 *Review* ({current_idx + 1}/{len(due_words)})\n\n" +
                format_word_card(word),
                parse_mode="Markdown",
                reply_markup=get_flashcard_keyboard(word_id)
            )
            return
    
    # Error case - skip to next
    await show_next_review_word(callback, state)
