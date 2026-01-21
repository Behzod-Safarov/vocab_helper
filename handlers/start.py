"""
Start Command Handler
Handles /start command and main menu navigation
"""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from storage.json_storage import get_or_create_user, UserDataManager
from keyboards.inline import get_main_menu_keyboard
from locales import get_text
import config

router = Router()


async def get_user_lang(user_id: int) -> str:
    """Get user's interface language"""
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    return user_manager.data.get("settings", {}).get("language", "en")


@router.message(Command("start"))
async def cmd_start(message: Message):
    """Handle /start command"""
    user_id = message.from_user.id
    username = message.from_user.username
    
    # Create or get user
    await get_or_create_user(user_id, username)
    
    # Get user language
    lang = await get_user_lang(user_id)
    
    await message.answer(
        get_text("welcome_message", lang),
        parse_mode="Markdown",
        reply_markup=get_main_menu_keyboard(lang)
    )


@router.callback_query(F.data == "menu:main")
async def show_main_menu(callback: CallbackQuery):
    """Show main menu"""
    user_id = callback.from_user.id
    lang = await get_user_lang(user_id)
    
    await callback.message.edit_text(
        get_text("main_menu_title", lang),
        parse_mode="Markdown",
        reply_markup=get_main_menu_keyboard(lang)
    )
    await callback.answer()


@router.message(Command("help"))
async def cmd_help(message: Message):
    """Handle /help command"""
    user_id = message.from_user.id
    lang = await get_user_lang(user_id)
    
    help_text = get_text("help_title", lang) + get_text("help_commands", lang)
    await message.answer(help_text, parse_mode="Markdown", reply_markup=get_main_menu_keyboard(lang))
