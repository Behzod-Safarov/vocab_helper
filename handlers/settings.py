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
    get_language_selection_keyboard,
    get_translation_selection_keyboard,
    get_back_button,
)
from locales import get_text
import config

router = Router()


async def get_user_lang(user_id: int) -> str:
    """Get user's interface language"""
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    return user_manager.data.get("settings", {}).get("language", "en")


@router.message(Command("settings"))
async def cmd_settings(message: Message):
    """Handle /settings command"""
    user_id = message.from_user.id
    
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    
    settings = user_manager.data.get("settings", {})
    lang = settings.get("language", "en")
    
    await message.answer(
        get_text("settings_title", lang),
        parse_mode="Markdown",
        reply_markup=get_settings_keyboard(settings, lang)
    )


@router.callback_query(F.data == "menu:settings")
async def show_settings_menu(callback: CallbackQuery):
    """Show settings menu"""
    user_id = callback.from_user.id
    
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    
    settings = user_manager.data.get("settings", {})
    lang = settings.get("language", "en")
    
    await callback.message.edit_text(
        get_text("settings_title", lang),
        parse_mode="Markdown",
        reply_markup=get_settings_keyboard(settings, lang)
    )
    await callback.answer()


# ============ Language Settings ============

@router.callback_query(F.data == "settings:language")
async def select_language(callback: CallbackQuery):
    """Show language selection"""
    user_id = callback.from_user.id
    lang = await get_user_lang(user_id)
    
    await callback.message.edit_text(
        get_text("select_language", lang),
        parse_mode="Markdown",
        reply_markup=get_language_selection_keyboard(lang)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("settings:setlang:"))
async def set_language(callback: CallbackQuery):
    """Set interface language"""
    new_lang = callback.data.split(":")[-1]
    user_id = callback.from_user.id
    
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    
    user_manager.data["settings"]["language"] = new_lang
    await user_manager.save()
    
    await callback.answer(get_text("language_changed", new_lang))
    
    settings = user_manager.data.get("settings", {})
    await callback.message.edit_text(
        get_text("settings_title", new_lang),
        parse_mode="Markdown",
        reply_markup=get_settings_keyboard(settings, new_lang)
    )


@router.callback_query(F.data == "settings:translation")
async def select_translation(callback: CallbackQuery):
    """Show translation language selection"""
    user_id = callback.from_user.id
    
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    
    settings = user_manager.data.get("settings", {})
    lang = settings.get("language", "en")
    current_trans = settings.get("translation_language", "both")
    
    await callback.message.edit_text(
        get_text("select_translation", lang),
        parse_mode="Markdown",
        reply_markup=get_translation_selection_keyboard(current_trans, lang)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("settings:settrans:"))
async def set_translation(callback: CallbackQuery):
    """Set translation language"""
    trans_lang = callback.data.split(":")[-1]
    user_id = callback.from_user.id
    
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    
    user_manager.data["settings"]["translation_language"] = trans_lang
    await user_manager.save()
    
    lang = user_manager.data["settings"].get("language", "en")
    await callback.answer(get_text("translation_changed", lang))
    
    settings = user_manager.data.get("settings", {})
    await callback.message.edit_text(
        get_text("settings_title", lang),
        parse_mode="Markdown",
        reply_markup=get_settings_keyboard(settings, lang)
    )


# ============ Other Settings ============

@router.callback_query(F.data == "settings:toggle_notif")
async def toggle_notifications(callback: CallbackQuery):
    """Toggle notifications"""
    user_id = callback.from_user.id
    
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    
    settings = user_manager.data.get("settings", {})
    lang = settings.get("language", "en")
    current = settings.get("notifications_enabled", True)
    settings["notifications_enabled"] = not current
    
    await user_manager.save()
    
    status = get_text("notifications_on", lang) if settings["notifications_enabled"] else get_text("notifications_off", lang)
    await callback.answer(f"Notifications {status}")
    
    await callback.message.edit_reply_markup(
        reply_markup=get_settings_keyboard(settings, lang)
    )


@router.callback_query(F.data == "settings:daily_words")
async def set_daily_words(callback: CallbackQuery):
    """Set daily new words count"""
    user_id = callback.from_user.id
    
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    
    settings = user_manager.data.get("settings", {})
    lang = settings.get("language", "en")
    current = settings.get("daily_new_words", 10)
    
    await callback.message.edit_text(
        get_text("daily_words_title", lang),
        parse_mode="Markdown",
        reply_markup=get_number_selection_keyboard(
            "setdaily",
            [5, 10, 15, 20, 25, 30],
            current,
            lang
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
    
    lang = user_manager.data["settings"].get("language", "en")
    await callback.answer(f"Daily words set to {value}")
    
    await callback.message.edit_text(
        get_text("settings_title", lang),
        parse_mode="Markdown",
        reply_markup=get_settings_keyboard(user_manager.data["settings"], lang)
    )


@router.callback_query(F.data == "settings:review_words")
async def set_review_words(callback: CallbackQuery):
    """Set daily review words count"""
    user_id = callback.from_user.id
    
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    
    settings = user_manager.data.get("settings", {})
    lang = settings.get("language", "en")
    current = settings.get("daily_review_words", 20)
    
    await callback.message.edit_text(
        get_text("daily_review_title", lang),
        parse_mode="Markdown",
        reply_markup=get_number_selection_keyboard(
            "setreview",
            [10, 20, 30, 40, 50, 60],
            current,
            lang
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
    
    lang = user_manager.data["settings"].get("language", "en")
    await callback.answer(f"Daily review set to {value}")
    
    await callback.message.edit_text(
        get_text("settings_title", lang),
        parse_mode="Markdown",
        reply_markup=get_settings_keyboard(user_manager.data["settings"], lang)
    )


@router.callback_query(F.data == "settings:reminder_time")
async def set_reminder_time(callback: CallbackQuery):
    """Set reminder time"""
    user_id = callback.from_user.id
    lang = await get_user_lang(user_id)
    
    await callback.message.edit_text(
        get_text("reminder_time_title", lang),
        parse_mode="Markdown",
        reply_markup=get_number_selection_keyboard(
            "settime",
            ["06:00", "08:00", "09:00", "10:00", "12:00", 
             "14:00", "18:00", "20:00", "21:00"],
            None,
            lang
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
    
    lang = user_manager.data["settings"].get("language", "en")
    await callback.answer(f"Reminder time set to {value}")
    
    await callback.message.edit_text(
        get_text("settings_title", lang),
        parse_mode="Markdown",
        reply_markup=get_settings_keyboard(user_manager.data["settings"], lang)
    )
