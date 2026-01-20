"""
Stats Command Handler
Handles /stats command and statistics display
"""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from storage.json_storage import UserDataManager
from modules.progress import (
    ProgressTracker,
    format_stats_message,
    format_level_progress,
    format_streak_message,
)
from keyboards.inline import (
    get_stats_menu_keyboard,
    get_level_stats_keyboard,
    get_back_button,
)
import config

router = Router()


@router.message(Command("stats"))
async def cmd_stats(message: Message):
    """Handle /stats command"""
    user_id = message.from_user.id
    
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    
    tracker = ProgressTracker(user_manager.data)
    stats = tracker.get_overall_stats()
    
    await message.answer(
        format_stats_message(stats),
        parse_mode="Markdown",
        reply_markup=get_stats_menu_keyboard()
    )


@router.callback_query(F.data == "menu:stats")
async def show_stats_menu(callback: CallbackQuery):
    """Show stats menu"""
    user_id = callback.from_user.id
    
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    
    tracker = ProgressTracker(user_manager.data)
    stats = tracker.get_overall_stats()
    
    await callback.message.edit_text(
        format_stats_message(stats),
        parse_mode="Markdown",
        reply_markup=get_stats_menu_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "stats:overall")
async def show_overall_stats(callback: CallbackQuery):
    """Show overall statistics"""
    user_id = callback.from_user.id
    
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    
    tracker = ProgressTracker(user_manager.data)
    stats = tracker.get_overall_stats()
    
    await callback.message.edit_text(
        format_stats_message(stats),
        parse_mode="Markdown",
        reply_markup=get_stats_menu_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "stats:levels")
async def show_level_selection(callback: CallbackQuery):
    """Show level selection for progress"""
    await callback.message.edit_text(
        "📘 *Level Progress*\n\nSelect a level to view progress:",
        parse_mode="Markdown",
        reply_markup=get_level_stats_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data.startswith("stats:level:"))
async def show_level_progress(callback: CallbackQuery):
    """Show progress for a specific level"""
    level = int(callback.data.split(":")[-1])
    user_id = callback.from_user.id
    
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    
    tracker = ProgressTracker(user_manager.data)
    progress = tracker.get_level_progress(level)
    
    await callback.message.edit_text(
        format_level_progress(progress),
        parse_mode="Markdown",
        reply_markup=get_back_button("stats:levels")
    )
    await callback.answer()


@router.callback_query(F.data == "stats:streak")
async def show_streak_info(callback: CallbackQuery):
    """Show streak information"""
    user_id = callback.from_user.id
    
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    
    tracker = ProgressTracker(user_manager.data)
    streak_info = tracker.get_streak_info()
    
    await callback.message.edit_text(
        format_streak_message(streak_info),
        parse_mode="Markdown",
        reply_markup=get_back_button("menu:stats")
    )
    await callback.answer()


@router.callback_query(F.data == "stats:weak")
async def show_weak_words_stats(callback: CallbackQuery):
    """Show weak words statistics"""
    user_id = callback.from_user.id
    
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    
    tracker = ProgressTracker(user_manager.data)
    weak_summary = tracker.get_weak_words_summary()
    
    if weak_summary["total_weak"] == 0:
        text = (
            "✨ *Weak Words*\n\n"
            "Great job! You don't have any weak words.\n\n"
            "Keep practicing to maintain your knowledge!"
        )
    else:
        text = (
            f"⚠️ *Weak Words Summary*\n\n"
            f"Total weak words: *{weak_summary['total_weak']}*\n\n"
        )
        
        if weak_summary["needs_attention"]:
            text += "⚡ These words need your attention!\n"
            text += "Consider taking a review test.\n"
    
    await callback.message.edit_text(
        text,
        parse_mode="Markdown",
        reply_markup=get_back_button("menu:stats")
    )
    await callback.answer()
