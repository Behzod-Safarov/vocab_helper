"""
Start Command Handler
Handles /start command and main menu navigation
"""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from storage.json_storage import get_or_create_user
from keyboards.inline import get_main_menu_keyboard
import config

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    """Handle /start command"""
    user_id = message.from_user.id
    username = message.from_user.username
    
    # Create or get user
    await get_or_create_user(user_id, username)
    
    await message.answer(
        config.WELCOME_MESSAGE,
        parse_mode="Markdown",
        reply_markup=get_main_menu_keyboard()
    )


@router.callback_query(F.data == "menu:main")
async def show_main_menu(callback: CallbackQuery):
    """Show main menu"""
    await callback.message.edit_text(
        "📚 *Vocabulary Coach*\n\nWhat would you like to do?",
        parse_mode="Markdown",
        reply_markup=get_main_menu_keyboard()
    )
    await callback.answer()


@router.message(Command("help"))
async def cmd_help(message: Message):
    """Handle /help command"""
    help_text = """
📖 *Vocabulary Coach Help*

*Commands:*
/start - Start the bot
/learn - Start a learning session
/test - Take a vocabulary test
/review - Review words due today
/stats - View your progress
/4000words - Access 4000 Essential Words
/settings - Customize your experience

*How it works:*
1️⃣ Learn new words from 4000 Essential Words or add your own
2️⃣ Practice with flashcards and quizzes
3️⃣ Review words using spaced repetition
4️⃣ Track your progress and build streaks

*Tips:*
• Study a little every day for best results
• Don't skip reviews - they help you remember!
• Use the "I forgot" button honestly
• Try to complete one unit before moving on

Need more help? Just start exploring! 📚
"""
    await message.answer(help_text, parse_mode="Markdown", reply_markup=get_main_menu_keyboard())
