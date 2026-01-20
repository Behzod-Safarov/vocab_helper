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
import config

router = Router()


class TestStates(StatesGroup):
    """States for test session"""
    in_test = State()
    awaiting_fill_blank = State()


@router.message(Command("test"))
async def cmd_test(message: Message):
    """Handle /test command"""
    await message.answer(
        "📝 *Test Mode*\n\nChoose a test type:",
        parse_mode="Markdown",
        reply_markup=get_test_menu_keyboard()
    )


@router.callback_query(F.data == "menu:test")
async def show_test_menu(callback: CallbackQuery, state: FSMContext):
    """Show test menu"""
    await state.clear()
    await callback.message.edit_text(
        "📝 *Test Mode*\n\nChoose a test type:",
        parse_mode="Markdown",
        reply_markup=get_test_menu_keyboard()
    )
    await callback.answer()


# ============ Unit Test ============

@router.callback_query(F.data == "test:unit")
async def test_unit_select_level(callback: CallbackQuery):
    """Select level for unit test"""
    await callback.message.edit_text(
        "📝 *Unit Test*\n\nSelect a level:",
        parse_mode="Markdown",
        reply_markup=get_level_selection_keyboard("test")
    )
    await callback.answer()


@router.callback_query(F.data.startswith("test:level:"))
async def test_select_unit(callback: CallbackQuery):
    """Select unit for test"""
    parts = callback.data.split(":")
    level = int(parts[2])
    page = int(parts[4]) if len(parts) > 4 and parts[3] == "page" else 0
    
    await callback.message.edit_text(
        f"📝 *Level {level} Unit Test*\n\nSelect a unit:",
        parse_mode="Markdown",
        reply_markup=get_unit_selection_keyboard(level, "test", page)
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
    
    # Get words from the unit
    words = await get_unit_words(level, unit)
    
    if not words:
        await callback.message.edit_text(
            f"❌ No words found for Level {level} Unit {unit}.",
            reply_markup=get_back_button("test:unit")
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
            "❌ Could not generate test questions.",
            reply_markup=get_back_button("test:unit")
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
        format_question(question, progress),
        parse_mode="Markdown",
        reply_markup=get_quiz_answer_keyboard(question.options, question.question_id)
    )
    await callback.answer()


# ============ Level Test ============

@router.callback_query(F.data == "test:level")
async def test_level_select(callback: CallbackQuery):
    """Select level for level test"""
    await callback.message.edit_text(
        "📚 *Level Test*\n\n"
        "⚠️ This test covers ALL units in the level.\n\n"
        "Select a level:",
        parse_mode="Markdown",
        reply_markup=get_level_selection_keyboard("leveltest")
    )
    await callback.answer()


@router.callback_query(F.data.startswith("leveltest:level:"))
async def start_level_test(callback: CallbackQuery, state: FSMContext):
    """Start level test"""
    level = int(callback.data.split(":")[-1])
    user_id = callback.from_user.id
    
    # Get all words from level
    words = await get_all_words_in_level(level)
    
    if not words:
        await callback.message.edit_text(
            f"❌ No words found for Level {level}.",
            reply_markup=get_back_button("test:level")
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
            format_question(question, progress) + "\n\n_Type your answer:_",
            parse_mode="Markdown",
            reply_markup=get_back_button("menu:test")
        )
    else:
        await callback.message.edit_text(
            format_question(question, progress),
            parse_mode="Markdown",
            reply_markup=get_quiz_answer_keyboard(question.options, question.question_id)
        )
    
    await callback.answer()


# ============ Review Test ============

@router.callback_query(F.data == "test:review")
async def start_review_test(callback: CallbackQuery, state: FSMContext):
    """Start review test (weak/forgotten words)"""
    user_id = callback.from_user.id
    
    vocab_manager = VocabularyManager(user_id)
    await vocab_manager.initialize()
    
    # Get weak words
    weak_words = await vocab_manager.get_weak_words(limit=20)
    
    if not weak_words:
        await callback.message.edit_text(
            "✨ *No Weak Words!*\n\n"
            "Great job! You don't have any weak words to review.\n"
            "Keep learning to add more words!",
            parse_mode="Markdown",
            reply_markup=get_back_button("menu:test")
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
        "🔄 *Review Test*\n\n" + format_question(question, progress),
        parse_mode="Markdown",
        reply_markup=get_quiz_answer_keyboard(question.options, question.question_id)
    )
    await callback.answer()


# ============ Answer Handling ============

@router.callback_query(F.data.startswith("quiz:ans:"))
async def handle_quiz_answer(callback: CallbackQuery, state: FSMContext):
    """Handle quiz answer selection"""
    parts = callback.data.split(":")
    question_id = parts[2]
    answer_idx = int(parts[3])
    
    data = await state.get_data()
    session_data = data.get("test_session")
    
    if not session_data:
        await callback.message.edit_text(
            "❌ Session expired. Please start a new test.",
            reply_markup=get_back_button("menu:test")
        )
        await callback.answer()
        return
    
    session = TestSession.from_dict(session_data)
    question = session.get_current_question()
    
    if not question:
        await show_test_results(callback, state, session)
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
        result_text = f"✅ *Correct!*\n\n*{question.word}*: {correct_answer}"
        await callback.answer("✅ Correct!")
    else:
        result_text = (
            f"❌ *Incorrect*\n\n"
            f"Your answer: {selected_answer}\n"
            f"Correct answer: *{correct_answer}*\n\n"
            f"{get_random_encouragement()}"
        )
        await callback.answer("❌ Incorrect")
    
    await callback.message.edit_text(
        result_text,
        parse_mode="Markdown",
        reply_markup=get_quiz_continue_keyboard(is_correct)
    )


@router.callback_query(F.data == "quiz:next")
async def quiz_next_question(callback: CallbackQuery, state: FSMContext):
    """Show next quiz question"""
    data = await state.get_data()
    session_data = data.get("test_session")
    
    if not session_data:
        await callback.message.edit_text(
            "❌ Session expired. Please start a new test.",
            reply_markup=get_back_button("menu:test")
        )
        await callback.answer()
        return
    
    session = TestSession.from_dict(session_data)
    question = session.next_question()
    
    if not question:
        # Test completed
        await show_test_results(callback, state, session)
        return
    
    # Update session
    await state.update_data(test_session=session.to_dict())
    
    progress = session.get_progress()
    
    if question.question_type == QuestionType.FILL_BLANK:
        await state.set_state(TestStates.awaiting_fill_blank)
        await callback.message.edit_text(
            format_question(question, progress) + "\n\n_Type your answer:_",
            parse_mode="Markdown",
            reply_markup=get_back_button("quiz:end")
        )
    else:
        await callback.message.edit_text(
            format_question(question, progress),
            parse_mode="Markdown",
            reply_markup=get_quiz_answer_keyboard(question.options, question.question_id)
        )
    
    await callback.answer()


@router.message(TestStates.awaiting_fill_blank)
async def handle_fill_blank_answer(message: Message, state: FSMContext):
    """Handle fill-in-the-blank answer"""
    from modules.test_engine import evaluate_answer
    
    data = await state.get_data()
    session_data = data.get("test_session")
    
    if not session_data:
        await message.answer(
            "❌ Session expired. Please start a new test.",
            reply_markup=get_back_button("menu:test")
        )
        return
    
    session = TestSession.from_dict(session_data)
    question = session.get_current_question()
    
    if not question:
        await show_test_results_msg(message, state, session)
        return
    
    # Check answer
    user_answer = message.text.strip()
    is_correct = evaluate_answer(user_answer, question.correct_answer)
    
    session.results[question.word_id] = is_correct
    session.answers[question.question_id] = user_answer
    
    # Update word status
    user_id = message.from_user.id
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    await user_manager.update_word_status(question.word_id, question.is_4000, is_correct)
    await user_manager.update_stats(correct=is_correct)
    
    # Store updated session
    await state.update_data(test_session=session.to_dict())
    await state.set_state(TestStates.in_test)
    
    # Show result
    if is_correct:
        result_text = f"✅ *Correct!*\n\nThe word is: *{question.correct_answer}*"
    else:
        result_text = (
            f"❌ *Incorrect*\n\n"
            f"Your answer: {user_answer}\n"
            f"Correct answer: *{question.correct_answer}*\n\n"
            f"{get_random_encouragement()}"
        )
    
    await message.answer(
        result_text,
        parse_mode="Markdown",
        reply_markup=get_quiz_continue_keyboard(is_correct)
    )


@router.callback_query(F.data == "quiz:skip")
async def skip_question(callback: CallbackQuery, state: FSMContext):
    """Skip current question"""
    data = await state.get_data()
    session_data = data.get("test_session")
    
    if not session_data:
        await callback.answer("Session expired")
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
        await show_test_results(callback, state, session)
        return
    
    progress = session.get_progress()
    
    await callback.message.edit_text(
        format_question(question, progress),
        parse_mode="Markdown",
        reply_markup=get_quiz_answer_keyboard(question.options, question.question_id)
    )
    await callback.answer("Skipped")


@router.callback_query(F.data.startswith("quiz:hint:"))
async def show_hint(callback: CallbackQuery, state: FSMContext):
    """Show hint for current question"""
    data = await state.get_data()
    session_data = data.get("test_session")
    
    if not session_data:
        await callback.answer("Session expired")
        return
    
    session = TestSession.from_dict(session_data)
    question = session.get_current_question()
    
    if question and question.hint:
        await callback.answer(f"💡 Hint: {question.hint}", show_alert=True)
    elif question and question.example:
        await callback.answer(f"💡 Example: {question.example}", show_alert=True)
    else:
        await callback.answer("No hint available", show_alert=True)


@router.callback_query(F.data == "quiz:end")
async def end_test_early(callback: CallbackQuery, state: FSMContext):
    """End test early"""
    data = await state.get_data()
    session_data = data.get("test_session")
    
    if session_data:
        session = TestSession.from_dict(session_data)
        await show_test_results(callback, state, session)
    else:
        await callback.message.edit_text(
            "Test ended.",
            reply_markup=get_test_menu_keyboard()
        )
        await state.clear()
    
    await callback.answer()


async def show_test_results(callback: CallbackQuery, state: FSMContext, session: TestSession):
    """Show test results"""
    result = session.get_results()
    
    # Update user stats
    user_id = callback.from_user.id
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    await user_manager.update_stats(correct=False, test_completed=True)
    
    await state.clear()
    
    await callback.message.edit_text(
        format_result(result),
        parse_mode="Markdown",
        reply_markup=get_test_result_keyboard()
    )


async def show_test_results_msg(message: Message, state: FSMContext, session: TestSession):
    """Show test results (from message handler)"""
    result = session.get_results()
    
    # Update user stats
    user_id = message.from_user.id
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    await user_manager.update_stats(correct=False, test_completed=True)
    
    await state.clear()
    
    await message.answer(
        format_result(result),
        parse_mode="Markdown",
        reply_markup=get_test_result_keyboard()
    )


@router.callback_query(F.data == "test:retry")
async def retry_test(callback: CallbackQuery):
    """Retry the same test - redirect to test menu"""
    await callback.message.edit_text(
        "📝 *Test Mode*\n\nChoose a test type:",
        parse_mode="Markdown",
        reply_markup=get_test_menu_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "test:details")
async def show_test_details(callback: CallbackQuery):
    """Show detailed test results"""
    await callback.answer("Detailed results coming soon!", show_alert=True)
