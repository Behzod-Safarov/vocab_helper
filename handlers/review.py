"""
Review Command Handler
Handles /review command and review functionality
"""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from storage.json_storage import UserDataManager
from modules.spaced_repetition import SpacedRepetitionScheduler
from keyboards.inline import get_review_menu_keyboard, get_back_button
from utils.helpers import get_random_motivation

router = Router()


@router.message(Command("review"))
async def cmd_review(message: Message):
    """Handle /review command"""
    user_id = message.from_user.id
    
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    
    scheduler = SpacedRepetitionScheduler(user_manager.data)
    due_words = scheduler.get_due_words()
    
    due_count = len(due_words)
    
    if due_count == 0:
        text = (
            "🔄 *Review Mode*\n\n"
            "✨ You're all caught up!\n\n"
            "No words are due for review right now.\n"
            "Keep learning new words or check back later!"
        )
    else:
        text = (
            "🔄 *Review Mode*\n\n"
            f"📚 You have *{due_count}* words due for review!\n\n"
            "Regular review helps you remember words better."
        )
    
    await message.answer(
        text,
        parse_mode="Markdown",
        reply_markup=get_review_menu_keyboard(due_count)
    )


@router.callback_query(F.data == "menu:review")
async def show_review_menu(callback: CallbackQuery):
    """Show review menu"""
    user_id = callback.from_user.id
    
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    
    scheduler = SpacedRepetitionScheduler(user_manager.data)
    due_words = scheduler.get_due_words()
    
    due_count = len(due_words)
    
    if due_count == 0:
        text = (
            "🔄 *Review Mode*\n\n"
            "✨ You're all caught up!\n"
            "No words due for review."
        )
    else:
        text = (
            "🔄 *Review Mode*\n\n"
            f"📚 *{due_count}* words due for review"
        )
    
    await callback.message.edit_text(
        text,
        parse_mode="Markdown",
        reply_markup=get_review_menu_keyboard(due_count)
    )
    await callback.answer()


@router.callback_query(F.data == "review:start")
async def start_review_session(callback: CallbackQuery, state: FSMContext):
    """Start review session - redirect to learn review"""
    # Redirect to the learn module's review functionality
    from handlers.learn import start_review
    await start_review(callback, state)


@router.callback_query(F.data == "review:weak")
async def show_weak_words(callback: CallbackQuery):
    """Show weak words that need attention"""
    user_id = callback.from_user.id
    
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    
    word_status = user_manager.data.get("words_4000_progress", {}).get("word_status", {})
    
    weak_words = []
    for word_id, status in word_status.items():
        if status.get("status") == "weak":
            weak_words.append(word_id)
    
    if not weak_words:
        await callback.message.edit_text(
            "⚠️ *Weak Words*\n\n"
            "✨ Great news! You don't have any weak words.\n\n"
            "Keep practicing to maintain your knowledge!",
            parse_mode="Markdown",
            reply_markup=get_back_button("menu:review")
        )
    else:
        # Parse some word IDs for display
        from utils.helpers import parse_word_id
        
        word_info = []
        for wid in weak_words[:10]:
            parsed = parse_word_id(wid)
            if parsed:
                word_info.append(f"• L{parsed['level']} U{parsed['unit']} W{parsed['word_index']}")
        
        await callback.message.edit_text(
            f"⚠️ *Weak Words* ({len(weak_words)} total)\n\n"
            f"These words need more practice:\n\n"
            f"{chr(10).join(word_info)}\n"
            f"{'...' if len(weak_words) > 10 else ''}\n\n"
            "Take a review test to practice them!",
            parse_mode="Markdown",
            reply_markup=get_back_button("menu:review")
        )
    
    await callback.answer()


@router.callback_query(F.data == "review:schedule")
async def show_review_schedule(callback: CallbackQuery):
    """Show upcoming review schedule"""
    user_id = callback.from_user.id
    
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    
    scheduler = SpacedRepetitionScheduler(user_manager.data)
    upcoming = scheduler.get_upcoming_reviews(days=7)
    
    # Format schedule
    schedule_lines = []
    from datetime import datetime
    
    for date, count in upcoming.items():
        day_date = datetime.fromisoformat(date)
        day_name = day_date.strftime("%a %d")
        
        if count > 0:
            bar = "█" * min(count, 10) + ("+" if count > 10 else "")
            schedule_lines.append(f"{day_name}: {bar} ({count})")
        else:
            schedule_lines.append(f"{day_name}: - (0)")
    
    await callback.message.edit_text(
        "📅 *Review Schedule (7 Days)*\n\n"
        f"```\n{chr(10).join(schedule_lines)}\n```\n\n"
        "Regular review helps you remember!",
        parse_mode="Markdown",
        reply_markup=get_back_button("menu:review")
    )
    await callback.answer()
