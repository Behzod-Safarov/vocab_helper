"""
Test Command Handler
Handles /test command and testing functionality
"""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from storage.json_storage import UserDataManager, get_unit_words, get_all_words_in_level
from modules.test_engine import (
    TestSession, QuestionGenerator, QuestionType,
    format_question, format_result
)
from modules.vocabulary import VocabularyManager
from keyboards.inline import (
    get_test_menu_keyboard,
    get_level_selection_keyboard,
    get_unit_selection_keyboard,
    get_quiz_answer_keyboard,
    get_quiz_continue_keyboard,
    get_test_result_keyboard,
    get_back_button,
)
from utils.helpers import (
    get_random_motivation, get_random_encouragement,
    create_word_id, parse_word_id
)
from locales import get_text
import config

router = Router()


class TestStates(StatesGroup):
    """States for test session"""
    in_test = State()
    awaiting_fill_blank = State()


async def get_user_settings(user_id: int):
    """Get user language and translation settings"""
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    settings = user_manager.data.get("settings", {})
    lang = settings.get("language", "en")
    trans_lang = settings.get("translation_language", "both")
    return lang, trans_lang


@router.message(Command("test"))
async def cmd_test(message: Message):
    """Handle /test command"""
    user_id = message.from_user.id
    lang, trans_lang = await get_user_settings(user_id)
    
    await message.answer(
        get_text("test_menu_title", lang),
        parse_mode="Markdown",
        reply_markup=get_test_menu_keyboard(lang)
    )


@router.callback_query(F.data == "menu:test")
async def show_test_menu(callback: CallbackQuery, state: FSMContext):
    """Show test menu"""
    user_id = callback.from_user.id
    lang, trans_lang = await get_user_settings(user_id)
    
    await state.clear()
    await callback.message.edit_text(
        get_text("test_menu_title", lang),
        parse_mode="Markdown",
        reply_markup=get_test_menu_keyboard(lang)
    )
    await callback.answer()


# ============ Unit Test ============

@router.callback_query(F.data == "test:unit")
async def test_unit_select_level(callback: CallbackQuery):
    """Select level for unit test"""
    user_id = callback.from_user.id
    lang, trans_lang = await get_user_settings(user_id)
    
    await callback.message.edit_text(
        get_text("test_unit_select_level", lang),
        parse_mode="Markdown",
        reply_markup=get_level_selection_keyboard("test", lang)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("test:level:"))
async def test_select_unit(callback: CallbackQuery):
    """Select unit for test"""
    user_id = callback.from_user.id
    lang, trans_lang = await get_user_settings(user_id)
    
    parts = callback.data.split(":")
    level = int(parts[2])
    page = int(parts[4]) if len(parts) > 4 and parts[3] == "page" else 0
    
    await callback.message.edit_text(
        get_text("test_level_unit_select", lang, level=level),
        parse_mode="Markdown",
        reply_markup=get_unit_selection_keyboard(level, "test", page, lang)
    )
    await callback.answer()


@router.callback_query(F.data.regexp(r"^test:L(\d+)U(\d+)$"))
async def start_unit_test(callback: CallbackQuery, state: FSMContext):
    """Start unit test"""
    import re
    match = re.match(r"^test:L(\d+)U(\d+)$", callback.data)
    level = int(match.group(1))
    unit = int(match.group(2))
    
    user_id = callback.from_user.id
    lang, trans_lang = await get_user_settings(user_id)
    
    # Get words from the unit
    words = await get_unit_words(level, unit)
    
    if not words:
        await callback.message.edit_text(
            get_text("error_no_words", lang, level=level, unit=unit),
            reply_markup=get_back_button("test:unit", lang)
        )
        await callback.answer()
        return
    
    # Add word IDs and metadata
    for i, word in enumerate(words):
        word["word_id"] = create_word_id(level, unit, i)
        word["is_4000"] = True
        word["level"] = level
        word["unit"] = unit
    
    # Generate test
    generator = QuestionGenerator(words)
    questions = generator.generate_test(
        words,
        num_questions=min(config.WORDS_PER_QUIZ, len(words)),
        question_types=[
            QuestionType.WORD_TO_MEANING,
            QuestionType.MEANING_TO_WORD,
        ]
    )
    
    if not questions:
        await callback.message.edit_text(
            get_text("test_generate_error", lang),
            reply_markup=get_back_button("test:unit", lang)
        )
        await callback.answer()
        return
    
    # Create test session
    session = TestSession(user_id, "unit", level, unit)
    session.add_questions(questions)
    
    # Store session in state
    await state.set_state(TestStates.in_test)
    await state.update_data(test_session=session.to_dict())
    
    # Show first question
    question = session.get_current_question()
    progress = session.get_progress()
    
    await callback.message.edit_text(
        format_question(question, progress, lang),
        parse_mode="Markdown",
        reply_markup=get_quiz_answer_keyboard(question.options, question.question_id, lang)
    )
    await callback.answer()


# ============ Level Test ============

@router.callback_query(F.data == "test:level")
async def test_level_select(callback: CallbackQuery):
    """Select level for level test"""
    user_id = callback.from_user.id
    lang, trans_lang = await get_user_settings(user_id)
    
    await callback.message.edit_text(
        get_text("test_level_select", lang),
        parse_mode="Markdown",
        reply_markup=get_level_selection_keyboard("leveltest", lang)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("leveltest:level:"))
async def start_level_test(callback: CallbackQuery, state: FSMContext):
    """Start level test"""
    level = int(callback.data.split(":")[-1])
    user_id = callback.from_user.id
    lang, trans_lang = await get_user_settings(user_id)
    
    # Get all words from level
    words = await get_all_words_in_level(level)
    
    if not words:
        await callback.message.edit_text(
            get_text("error_no_words_level", lang, level=level),
            reply_markup=get_back_button("test:level", lang)
        )
        await callback.answer()
        return
    
    # Add word IDs
    for word in words:
        word["word_id"] = create_word_id(level, word["unit"], words.index(word) % config.WORDS_PER_UNIT)
        word["is_4000"] = True
    
    # Generate test (20 random questions)
    import random
    sampled_words = random.sample(words, min(20, len(words)))
    
    generator = QuestionGenerator(words)
    questions = generator.generate_test(
        sampled_words,
        num_questions=20,
        question_types=[
            QuestionType.WORD_TO_MEANING,
            QuestionType.MEANING_TO_WORD,
            QuestionType.FILL_BLANK,
        ]
    )
    
    # Create test session
    session = TestSession(user_id, "level", level)
    session.add_questions(questions)
    
    # Store session
    await state.set_state(TestStates.in_test)
    await state.update_data(test_session=session.to_dict())
    
    # Show first question
    question = session.get_current_question()
    progress = session.get_progress()
    
    if question.question_type == QuestionType.FILL_BLANK:
        await state.set_state(TestStates.awaiting_fill_blank)
        await callback.message.edit_text(
            format_question(question, progress, lang) + f"\n\n_{get_text('type_your_answer', lang)}_",
            parse_mode="Markdown",
            reply_markup=get_back_button("menu:test", lang)
        )
    else:
        await callback.message.edit_text(
            format_question(question, progress, lang),
            parse_mode="Markdown",
            reply_markup=get_quiz_answer_keyboard(question.options, question.question_id, lang)
        )
    
    await callback.answer()


# ============ Review Test ============

@router.callback_query(F.data == "test:review")
async def start_review_test(callback: CallbackQuery, state: FSMContext):
    """Start review test (weak/forgotten words)"""
    user_id = callback.from_user.id
    lang, trans_lang = await get_user_settings(user_id)
    
    vocab_manager = VocabularyManager(user_id)
    await vocab_manager.initialize()
    
    # Get weak words
    weak_words = await vocab_manager.get_weak_words(limit=20)
    
    if not weak_words:
        await callback.message.edit_text(
            get_text("no_weak_words", lang),
            parse_mode="Markdown",
            reply_markup=get_back_button("menu:test", lang)
        )
        await callback.answer()
        return
    
    # Generate test
    generator = QuestionGenerator(weak_words)
    questions = generator.generate_test(
        weak_words,
        num_questions=min(10, len(weak_words)),
    )
    
    # Create test session
    session = TestSession(user_id, "review")
    session.add_questions(questions)
    
    # Store session
    await state.set_state(TestStates.in_test)
    await state.update_data(test_session=session.to_dict())
    
    # Show first question
    question = session.get_current_question()
    progress = session.get_progress()
    
    await callback.message.edit_text(
        get_text("review_test_title", lang) + "\n\n" + format_question(question, progress, lang),
        parse_mode="Markdown",
        reply_markup=get_quiz_answer_keyboard(question.options, question.question_id, lang)
    )
    await callback.answer()


# ============ Answer Handling ============

@router.callback_query(F.data.startswith("quiz:ans:"))
async def handle_quiz_answer(callback: CallbackQuery, state: FSMContext):
    """Handle quiz answer selection"""
    user_id = callback.from_user.id
    lang, trans_lang = await get_user_settings(user_id)
    
    parts = callback.data.split(":")
    question_id = parts[2]
    answer_idx = int(parts[3])
    
    data = await state.get_data()
    session_data = data.get("test_session")
    
    if not session_data:
        await callback.message.edit_text(
            get_text("session_expired", lang),
            reply_markup=get_back_button("menu:test", lang)
        )
        await callback.answer()
        return
    
    session = TestSession.from_dict(session_data)
    question = session.get_current_question()
    
    if not question:
        await show_test_results(callback, state, session, lang)
        return
    
    # Get the selected answer
    selected_answer = question.options[answer_idx] if answer_idx < len(question.options) else ""
    
    # Check answer
    is_correct, correct_answer = session.answer_current(selected_answer)
    
    # Update word status
    user_id = callback.from_user.id
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    await user_manager.update_word_status(question.word_id, question.is_4000, is_correct)
    await user_manager.update_stats(correct=is_correct)
    
    # Store updated session
    await state.update_data(test_session=session.to_dict())
    
    # Show result
    if is_correct:
        result_text = get_text("test_correct", lang) + f"*{question.word}*: {correct_answer}"
        await callback.answer(get_text("correct", lang))
    else:
        result_text = (
            get_text("test_wrong", lang) +
            f"{get_text('your_answer', lang)}: {selected_answer}\n"
            f"{get_text('correct_answer', lang)}: *{correct_answer}*\n\n"
            f"{get_random_encouragement(lang)}"
        )
        await callback.answer(get_text("incorrect", lang))
    
    await callback.message.edit_text(
        result_text,
        parse_mode="Markdown",
        reply_markup=get_quiz_continue_keyboard(is_correct, lang)
    )


@router.callback_query(F.data == "quiz:next")
async def quiz_next_question(callback: CallbackQuery, state: FSMContext):
    """Show next quiz question"""
    user_id = callback.from_user.id
    lang, trans_lang = await get_user_settings(user_id)
    
    data = await state.get_data()
    session_data = data.get("test_session")
    
    if not session_data:
        await callback.message.edit_text(
            get_text("session_expired", lang),
            reply_markup=get_back_button("menu:test", lang)
        )
        await callback.answer()
        return
    
    session = TestSession.from_dict(session_data)
    question = session.next_question()
    
    if not question:
        # Test completed
        await show_test_results(callback, state, session, lang)
        return
    
    # Update session
    await state.update_data(test_session=session.to_dict())
    
    progress = session.get_progress()
    
    if question.question_type == QuestionType.FILL_BLANK:
        await state.set_state(TestStates.awaiting_fill_blank)
        await callback.message.edit_text(
            format_question(question, progress, lang) + f"\n\n_{get_text('type_your_answer', lang)}_",
            parse_mode="Markdown",
            reply_markup=get_back_button("quiz:end", lang)
        )
    else:
        await callback.message.edit_text(
            format_question(question, progress, lang),
            parse_mode="Markdown",
            reply_markup=get_quiz_answer_keyboard(question.options, question.question_id, lang)
        )
    
    await callback.answer()


@router.message(TestStates.awaiting_fill_blank)
async def handle_fill_blank_answer(message: Message, state: FSMContext):
    """Handle fill-in-the-blank answer"""
    from modules.test_engine import evaluate_answer
    
    user_id = message.from_user.id
    lang, trans_lang = await get_user_settings(user_id)
    
    data = await state.get_data()
    session_data = data.get("test_session")
    
    if not session_data:
        await message.answer(
            get_text("session_expired", lang),
            reply_markup=get_back_button("menu:test", lang)
        )
        return
    
    session = TestSession.from_dict(session_data)
    question = session.get_current_question()
    
    if not question:
        await show_test_results_msg(message, state, session, lang)
        return
    
    # Check answer
    user_answer = message.text.strip()
    is_correct = evaluate_answer(user_answer, question.correct_answer)
    
    session.results[question.word_id] = is_correct
    session.answers[question.question_id] = user_answer
    
    # Update word status
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    await user_manager.update_word_status(question.word_id, question.is_4000, is_correct)
    await user_manager.update_stats(correct=is_correct)
    
    # Store updated session
    await state.update_data(test_session=session.to_dict())
    await state.set_state(TestStates.in_test)
    
    # Show result
    if is_correct:
        result_text = get_text("test_correct", lang) + f"{get_text('the_word_is', lang)}: *{question.correct_answer}*"
    else:
        result_text = (
            get_text("test_wrong", lang) +
            f"{get_text('your_answer', lang)}: {user_answer}\n"
            f"{get_text('correct_answer', lang)}: *{question.correct_answer}*\n\n"
            f"{get_random_encouragement(lang)}"
        )
    
    await message.answer(
        result_text,
        parse_mode="Markdown",
        reply_markup=get_quiz_continue_keyboard(is_correct, lang)
    )


@router.callback_query(F.data.startswith("quiz:skip:"))
async def skip_question(callback: CallbackQuery, state: FSMContext):
    """Skip current question"""
    user_id = callback.from_user.id
    lang, trans_lang = await get_user_settings(user_id)
    
    data = await state.get_data()
    session_data = data.get("test_session")
    
    if not session_data:
        await callback.answer(get_text("session_expired", lang))
        return
    
    session = TestSession.from_dict(session_data)
    question = session.get_current_question()
    
    if question:
        # Mark as wrong
        session.results[question.word_id] = False
        session.answers[question.question_id] = ""
    
    # Move to next
    question = session.next_question()
    await state.update_data(test_session=session.to_dict())
    
    if not question:
        await show_test_results(callback, state, session, lang)
        return
    
    progress = session.get_progress()
    
    await callback.message.edit_text(
        format_question(question, progress, lang),
        parse_mode="Markdown",
        reply_markup=get_quiz_answer_keyboard(question.options, question.question_id, lang)
    )
    await callback.answer(get_text("skipped", lang))


@router.callback_query(F.data.startswith("quiz:hint:"))
async def show_hint(callback: CallbackQuery, state: FSMContext):
    """Show hint for current question"""
    user_id = callback.from_user.id
    lang, trans_lang = await get_user_settings(user_id)
    
    data = await state.get_data()
    session_data = data.get("test_session")
    
    if not session_data:
        await callback.answer(get_text("session_expired", lang))
        return
    
    session = TestSession.from_dict(session_data)
    question = session.get_current_question()
    
    if question and question.hint:
        await callback.answer(f"💡 {get_text('hint', lang)}: {question.hint}", show_alert=True)
    elif question and question.example:
        await callback.answer(f"💡 {get_text('example', lang)}: {question.example}", show_alert=True)
    else:
        await callback.answer(get_text("no_hint", lang), show_alert=True)


@router.callback_query(F.data == "quiz:end")
async def end_test_early(callback: CallbackQuery, state: FSMContext):
    """End test early"""
    user_id = callback.from_user.id
    lang, trans_lang = await get_user_settings(user_id)
    
    data = await state.get_data()
    session_data = data.get("test_session")
    
    if session_data:
        session = TestSession.from_dict(session_data)
        await show_test_results(callback, state, session, lang)
    else:
        await callback.message.edit_text(
            get_text("test_ended", lang),
            reply_markup=get_test_menu_keyboard(lang)
        )
        await state.clear()
    
    await callback.answer()


async def show_test_results(callback: CallbackQuery, state: FSMContext, session: TestSession, lang: str = "en"):
    """Show test results"""
    result = session.get_results()
    
    # Update user stats
    user_id = callback.from_user.id
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    await user_manager.update_stats(correct=False, test_completed=True)
    
    await state.clear()
    
    await callback.message.edit_text(
        format_result(result, lang),
        parse_mode="Markdown",
        reply_markup=get_test_result_keyboard(lang)
    )


async def show_test_results_msg(message: Message, state: FSMContext, session: TestSession, lang: str = "en"):
    """Show test results (from message handler)"""
    result = session.get_results()
    
    # Update user stats
    user_id = message.from_user.id
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    await user_manager.update_stats(correct=False, test_completed=True)
    
    await state.clear()
    
    await message.answer(
        format_result(result, lang),
        parse_mode="Markdown",
        reply_markup=get_test_result_keyboard(lang)
    )


@router.callback_query(F.data == "test:retry")
async def retry_test(callback: CallbackQuery):
    """Retry the same test - redirect to test menu"""
    user_id = callback.from_user.id
    lang, trans_lang = await get_user_settings(user_id)
    
    await callback.message.edit_text(
        get_text("test_menu_title", lang),
        parse_mode="Markdown",
        reply_markup=get_test_menu_keyboard(lang)
    )
    await callback.answer()


@router.callback_query(F.data == "test:details")
async def show_test_details(callback: CallbackQuery):
    """Show detailed test results"""
    user_id = callback.from_user.id
    lang, trans_lang = await get_user_settings(user_id)
    
    await callback.answer(get_text("coming_soon", lang), show_alert=True)
