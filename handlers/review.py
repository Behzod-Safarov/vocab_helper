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
from locales import get_text

router = Router()


async def get_user_settings(user_id: int):
    """Get user language and translation settings"""
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    settings = user_manager.data.get("settings", {})
    lang = settings.get("language", "en")
    trans_lang = settings.get("translation_language", "both")
    return lang, trans_lang


@router.message(Command("review"))
async def cmd_review(message: Message):
    """Handle /review command"""
    user_id = message.from_user.id
    lang, trans_lang = await get_user_settings(user_id)
    
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    
    scheduler = SpacedRepetitionScheduler(user_manager.data)
    due_words = scheduler.get_due_words()
    
    due_count = len(due_words)
    
    if due_count == 0:
        text = get_text("review_no_words_due", lang)
    else:
        text = get_text("review_words_due", lang, count=due_count)
    
    await message.answer(
        text,
        parse_mode="Markdown",
        reply_markup=get_review_menu_keyboard(due_count, lang)
    )


@router.callback_query(F.data == "menu:review")
async def show_review_menu(callback: CallbackQuery):
    """Show review menu"""
    user_id = callback.from_user.id
    lang, trans_lang = await get_user_settings(user_id)
    
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    
    scheduler = SpacedRepetitionScheduler(user_manager.data)
    due_words = scheduler.get_due_words()
    
    due_count = len(due_words)
    
    if due_count == 0:
        text = get_text("review_no_words_due_short", lang)
    else:
        text = get_text("review_words_due_short", lang, count=due_count)
    
    await callback.message.edit_text(
        text,
        parse_mode="Markdown",
        reply_markup=get_review_menu_keyboard(due_count, lang)
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
    lang, trans_lang = await get_user_settings(user_id)
    
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    
    word_status = user_manager.data.get("words_4000_progress", {}).get("word_status", {})
    
    weak_words = []
    for word_id, status in word_status.items():
        if status.get("status") == "weak":
            weak_words.append(word_id)
    
    if not weak_words:
        await callback.message.edit_text(
            get_text("no_weak_words_review", lang),
            parse_mode="Markdown",
            reply_markup=get_back_button("menu:review", lang)
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
            get_text("weak_words_list", lang, count=len(weak_words), word_list=chr(10).join(word_info), more="..." if len(weak_words) > 10 else ""),
            parse_mode="Markdown",
            reply_markup=get_back_button("menu:review", lang)
        )
    
    await callback.answer()


@router.callback_query(F.data == "review:schedule")
async def show_review_schedule(callback: CallbackQuery):
    """Show upcoming review schedule"""
    user_id = callback.from_user.id
    lang, trans_lang = await get_user_settings(user_id)
    
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
        get_text("review_schedule_title", lang) + f"\n\n```\n{chr(10).join(schedule_lines)}\n```\n\n" + get_text("review_schedule_tip", lang),
        parse_mode="Markdown",
        reply_markup=get_back_button("menu:review", lang)
    )
    await callback.answer()
