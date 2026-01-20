"""
Settings Command Handler
Handles /settings command and user preferences
"""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from storage.json_storage import UserDataManager
from keyboards.inline import (
    get_settings_keyboard,
    get_number_selection_keyboard,
    get_back_button,
)
import config

router = Router()


@router.message(Command("settings"))
async def cmd_settings(message: Message):
    """Handle /settings command"""
    user_id = message.from_user.id
    
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    
    settings = user_manager.data.get("settings", {})
    
    await message.answer(
        "⚙️ *Settings*\n\nCustomize your learning experience:",
        parse_mode="Markdown",
        reply_markup=get_settings_keyboard(settings)
    )


@router.callback_query(F.data == "menu:settings")
async def show_settings_menu(callback: CallbackQuery):
    """Show settings menu"""
    user_id = callback.from_user.id
    
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    
    settings = user_manager.data.get("settings", {})
    
    await callback.message.edit_text(
        "⚙️ *Settings*\n\nCustomize your learning experience:",
        parse_mode="Markdown",
        reply_markup=get_settings_keyboard(settings)
    )
    await callback.answer()


@router.callback_query(F.data == "settings:toggle_notif")
async def toggle_notifications(callback: CallbackQuery):
    """Toggle notifications"""
    user_id = callback.from_user.id
    
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    
    settings = user_manager.data.get("settings", {})
    current = settings.get("notifications_enabled", True)
    settings["notifications_enabled"] = not current
    
    await user_manager.save()
    
    status = "enabled" if settings["notifications_enabled"] else "disabled"
    await callback.answer(f"Notifications {status}")
    
    await callback.message.edit_reply_markup(
        reply_markup=get_settings_keyboard(settings)
    )


@router.callback_query(F.data == "settings:daily_words")
async def set_daily_words(callback: CallbackQuery):
    """Set daily new words count"""
    user_id = callback.from_user.id
    
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    
    current = user_manager.data.get("settings", {}).get("daily_new_words", 10)
    
    await callback.message.edit_text(
        "📚 *Daily New Words*\n\n"
        "How many new words do you want to learn per day?",
        parse_mode="Markdown",
        reply_markup=get_number_selection_keyboard(
            "setdaily",
            [5, 10, 15, 20, 25, 30],
            current
        )
    )
    await callback.answer()


@router.callback_query(F.data.startswith("setdaily:"))
async def save_daily_words(callback: CallbackQuery):
    """Save daily words setting"""
    value = int(callback.data.split(":")[-1])
    user_id = callback.from_user.id
    
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    
    user_manager.data["settings"]["daily_new_words"] = value
    await user_manager.save()
    
    await callback.answer(f"Daily words set to {value}")
    
    await callback.message.edit_text(
        "⚙️ *Settings*\n\nCustomize your learning experience:",
        parse_mode="Markdown",
        reply_markup=get_settings_keyboard(user_manager.data["settings"])
    )


@router.callback_query(F.data == "settings:review_words")
async def set_review_words(callback: CallbackQuery):
    """Set daily review words count"""
    user_id = callback.from_user.id
    
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    
    current = user_manager.data.get("settings", {}).get("daily_review_words", 20)
    
    await callback.message.edit_text(
        "🔄 *Daily Review Words*\n\n"
        "How many words do you want to review per day?",
        parse_mode="Markdown",
        reply_markup=get_number_selection_keyboard(
            "setreview",
            [10, 20, 30, 40, 50, 60],
            current
        )
    )
    await callback.answer()


@router.callback_query(F.data.startswith("setreview:"))
async def save_review_words(callback: CallbackQuery):
    """Save review words setting"""
    value = int(callback.data.split(":")[-1])
    user_id = callback.from_user.id
    
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    
    user_manager.data["settings"]["daily_review_words"] = value
    await user_manager.save()
    
    await callback.answer(f"Daily review set to {value}")
    
    await callback.message.edit_text(
        "⚙️ *Settings*\n\nCustomize your learning experience:",
        parse_mode="Markdown",
        reply_markup=get_settings_keyboard(user_manager.data["settings"])
    )


@router.callback_query(F.data == "settings:reminder_time")
async def set_reminder_time(callback: CallbackQuery):
    """Set reminder time"""
    await callback.message.edit_text(
        "⏰ *Reminder Time*\n\n"
        "Select when you'd like to receive daily reminders:",
        parse_mode="Markdown",
        reply_markup=get_number_selection_keyboard(
            "settime",
            ["06:00", "08:00", "09:00", "10:00", "12:00", 
             "14:00", "18:00", "20:00", "21:00"],
            None
        )
    )
    await callback.answer()


@router.callback_query(F.data.startswith("settime:"))
async def save_reminder_time(callback: CallbackQuery):
    """Save reminder time setting"""
    value = callback.data.split(":")[-1] + ":00"
    user_id = callback.from_user.id
    
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    
    user_manager.data["settings"]["notification_time"] = value
    await user_manager.save()
    
    await callback.answer(f"Reminder time set to {value}")
    
    await callback.message.edit_text(
        "⚙️ *Settings*\n\nCustomize your learning experience:",
        parse_mode="Markdown",
        reply_markup=get_settings_keyboard(user_manager.data["settings"])
    )
