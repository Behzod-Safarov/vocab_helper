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
from utils.helpers import safe_edit_text
from locales import get_text
import config

router = Router()


async def get_user_settings(user_id: int):
    """Get user language and translation settings"""
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    settings = user_manager.data.get("settings", {})
    lang = settings.get("language", "en")
    trans_lang = settings.get("translation_language", "both")
    return lang, trans_lang


@router.message(Command("stats"))
async def cmd_stats(message: Message):
    """Handle /stats command"""
    user_id = message.from_user.id
    lang, trans_lang = await get_user_settings(user_id)
    
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    
    tracker = ProgressTracker(user_manager.data)
    stats = tracker.get_overall_stats()
    
    await message.answer(
        format_stats_message(stats, lang),
        parse_mode="Markdown",
        reply_markup=get_stats_menu_keyboard(lang)
    )


@router.callback_query(F.data == "menu:stats")
async def show_stats_menu(callback: CallbackQuery):
    """Show stats menu"""
    user_id = callback.from_user.id
    lang, trans_lang = await get_user_settings(user_id)
    
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    
    tracker = ProgressTracker(user_manager.data)
    stats = tracker.get_overall_stats()
    
    await callback.message.edit_text(
        format_stats_message(stats, lang),
        parse_mode="Markdown",
        reply_markup=get_stats_menu_keyboard(lang)
    )
    await callback.answer()


@router.callback_query(F.data == "stats:overall")
async def show_overall_stats(callback: CallbackQuery):
    """Show overall statistics"""
    user_id = callback.from_user.id
    lang, trans_lang = await get_user_settings(user_id)
    
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    
    tracker = ProgressTracker(user_manager.data)
    stats = tracker.get_overall_stats()
    
    await safe_edit_text(
        callback.message,
        format_stats_message(stats, lang),
        parse_mode="Markdown",
        reply_markup=get_stats_menu_keyboard(lang)
    )
    await callback.answer()


@router.callback_query(F.data == "stats:levels")
async def show_level_selection(callback: CallbackQuery):
    """Show level selection for progress"""
    user_id = callback.from_user.id
    lang, trans_lang = await get_user_settings(user_id)
    
    await callback.message.edit_text(
        get_text("level_progress_title", lang),
        parse_mode="Markdown",
        reply_markup=get_level_stats_keyboard(lang)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("stats:level:"))
async def show_level_progress(callback: CallbackQuery):
    """Show progress for a specific level"""
    level = int(callback.data.split(":")[-1])
    user_id = callback.from_user.id
    lang, trans_lang = await get_user_settings(user_id)
    
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    
    tracker = ProgressTracker(user_manager.data)
    progress = tracker.get_level_progress(level)
    
    await callback.message.edit_text(
        format_level_progress(progress, lang),
        parse_mode="Markdown",
        reply_markup=get_back_button("stats:levels", lang)
    )
    await callback.answer()


@router.callback_query(F.data == "stats:streak")
async def show_streak_info(callback: CallbackQuery):
    """Show streak information"""
    user_id = callback.from_user.id
    lang, trans_lang = await get_user_settings(user_id)
    
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    
    tracker = ProgressTracker(user_manager.data)
    streak_info = tracker.get_streak_info()
    
    await callback.message.edit_text(
        format_streak_message(streak_info, lang),
        parse_mode="Markdown",
        reply_markup=get_back_button("menu:stats", lang)
    )
    await callback.answer()


@router.callback_query(F.data == "stats:weak")
async def show_weak_words_stats(callback: CallbackQuery):
    """Show weak words statistics"""
    user_id = callback.from_user.id
    lang, trans_lang = await get_user_settings(user_id)
    
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    
    tracker = ProgressTracker(user_manager.data)
    weak_summary = tracker.get_weak_words_summary()
    
    if weak_summary["total_weak"] == 0:
        text = get_text("no_weak_words_stats", lang)
    else:
        text = get_text("weak_words_summary", lang, count=weak_summary['total_weak'])
        
        if weak_summary["needs_attention"]:
            text += "\n" + get_text("weak_words_attention", lang)
    
    await callback.message.edit_text(
        text,
        parse_mode="Markdown",
        reply_markup=get_back_button("menu:stats", lang)
    )
    await callback.answer()
