"""
4000 Words Command Handler
Handles /4000words command and 4000 Essential Words navigation
"""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from storage.json_storage import UserDataManager, load_4000_words_level
from modules.vocabulary import VocabularyManager
from modules.progress import ProgressTracker, format_level_progress
from keyboards.inline import (
    get_4000_words_menu_keyboard,
    get_level_selection_keyboard,
    get_unit_selection_keyboard,
    get_back_button,
)
from utils.helpers import get_level_description
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


@router.message(Command("4000words"))
async def cmd_4000words(message: Message):
    """Handle /4000words command"""
    user_id = message.from_user.id
    lang, trans_lang = await get_user_settings(user_id)
    
    await message.answer(
        get_text("4000_words_title", lang),
        parse_mode="Markdown",
        reply_markup=get_4000_words_menu_keyboard(lang)
    )


@router.callback_query(F.data == "menu:4000words")
async def show_4000_menu(callback: CallbackQuery):
    """Show 4000 words menu"""
    user_id = callback.from_user.id
    lang, trans_lang = await get_user_settings(user_id)
    
    await callback.message.edit_text(
        get_text("4000_words_menu", lang),
        parse_mode="Markdown",
        reply_markup=get_4000_words_menu_keyboard(lang)
    )
    await callback.answer()


@router.callback_query(F.data == "4000:browse")
async def browse_levels(callback: CallbackQuery):
    """Browse all levels"""
    user_id = callback.from_user.id
    lang, trans_lang = await get_user_settings(user_id)
    
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    
    tracker = ProgressTracker(user_manager.data)
    
    # Build level overview
    lines = [f"📘 *{get_text('4000_essential_words', lang)}*\n"]
    
    for level in range(1, config.LEVELS + 1):
        progress = tracker.get_level_progress(level)
        pct = progress.get("progress_percentage", 0)
        
        # Progress bar
        filled = int(pct / 10)
        bar = "█" * filled + "░" * (10 - filled)
        
        desc = get_level_description(level)
        lines.append(f"*{get_text('level', lang)} {level}*: {bar} {pct:.0f}%")
        lines.append(f"_{desc}_\n")
    
    await callback.message.edit_text(
        "\n".join(lines),
        parse_mode="Markdown",
        reply_markup=get_level_selection_keyboard("browse", lang)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("browse:level:"))
async def browse_level_units(callback: CallbackQuery):
    """Browse units in a level"""
    user_id = callback.from_user.id
    lang, trans_lang = await get_user_settings(user_id)
    
    parts = callback.data.split(":")
    level = int(parts[2])
    page = int(parts[4]) if len(parts) > 4 and parts[3] == "page" else 0
    
    vocab_manager = VocabularyManager(user_id)
    await vocab_manager.initialize()
    
    # Get level progress
    progress = await vocab_manager.get_user_progress_for_level(level)
    
    desc = get_level_description(level)
    
    await callback.message.edit_text(
        f"📘 *{get_text('level', lang)} {level}*\n"
        f"_{desc}_\n\n"
        f"📊 {get_text('progress', lang)}: {progress['completion_rate']:.1f}%\n"
        f"✅ {get_text('learned', lang)}: {progress['learned']}/{progress['total_words']}\n"
        f"⭐ {get_text('mastered', lang)}: {progress['mastered']}\n"
        f"⚠️ {get_text('weak', lang)}: {progress['weak']}\n\n"
        f"{get_text('select_unit', lang)}:",
        parse_mode="Markdown",
        reply_markup=get_unit_selection_keyboard(level, "browse", page, lang)
    )
    await callback.answer()


@router.callback_query(F.data.regexp(r"^browse:L(\d+)U(\d+)$"))
async def browse_unit_words(callback: CallbackQuery):
    """Browse words in a unit"""
    import re
    match = re.match(r"^browse:L(\d+)U(\d+)$", callback.data)
    level = int(match.group(1))
    unit = int(match.group(2))
    
    user_id = callback.from_user.id
    lang, trans_lang = await get_user_settings(user_id)
    
    vocab_manager = VocabularyManager(user_id)
    await vocab_manager.initialize()
    
    # Get unit words
    words = await vocab_manager.get_4000_unit_words(level, unit)
    
    if not words:
        await callback.message.edit_text(
            get_text("error_no_words", lang, level=level, unit=unit),
            reply_markup=get_back_button(f"browse:level:{level}", lang)
        )
        await callback.answer()
        return
    
    # Get unit progress
    progress = await vocab_manager.get_user_progress_for_unit(level, unit)
    
    # Build word list preview
    word_list = []
    for i, word in enumerate(words[:10]):
        word_list.append(f"• {word.get('word', 'Unknown')}")
    
    if len(words) > 10:
        word_list.append(f"...{get_text('and_more', lang, count=len(words) - 10)}")
    
    await callback.message.edit_text(
        f"📗 *{get_text('level', lang)} {level} • {get_text('unit', lang)} {unit}*\n\n"
        f"📊 {get_text('progress', lang)}: {progress['completion_rate']:.1f}%\n"
        f"📚 {get_text('words', lang)}: {progress['total']}\n"
        f"✅ {get_text('known', lang)}: {progress['known']}\n"
        f"⭐ {get_text('mastered', lang)}: {progress['mastered']}\n\n"
        f"*{get_text('words_in_unit', lang)}:*\n"
        + "\n".join(word_list),
        parse_mode="Markdown",
        reply_markup=get_back_button(f"browse:level:{level}", lang)
    )
    await callback.answer()


@router.callback_query(F.data == "4000:continue")
async def continue_learning(callback: CallbackQuery):
    """Continue learning from where user left off"""
    user_id = callback.from_user.id
    lang, trans_lang = await get_user_settings(user_id)
    
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    
    progress = user_manager.data.get("words_4000_progress", {})
    current_level = progress.get("current_level", 1)
    current_unit = progress.get("current_unit", 1)
    
    await callback.message.edit_text(
        get_text("continue_learning", lang, level=current_level, unit=current_unit),
        parse_mode="Markdown",
        reply_markup=get_back_button(f"learn:L{current_level}U{current_unit}", lang)
    )
    await callback.answer()


@router.callback_query(F.data == "4000:test")
async def test_4000(callback: CallbackQuery):
    """Redirect to test menu for 4000 words"""
    user_id = callback.from_user.id
    lang, trans_lang = await get_user_settings(user_id)
    
    from keyboards.inline import get_test_menu_keyboard
    
    await callback.message.edit_text(
        get_text("4000_test_title", lang),
        parse_mode="Markdown",
        reply_markup=get_test_menu_keyboard(lang)
    )
    await callback.answer()


@router.callback_query(F.data == "4000:progress")
async def show_4000_progress(callback: CallbackQuery):
    """Show overall 4000 words progress"""
    user_id = callback.from_user.id
    lang, trans_lang = await get_user_settings(user_id)
    
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    
    tracker = ProgressTracker(user_manager.data)
    
    # Calculate overall progress
    total_words = 0
    learned_words = 0
    mastered_words = 0
    
    lines = [f"📊 *{get_text('4000_progress_title', lang)}*\n"]
    
    for level in range(1, config.LEVELS + 1):
        progress = tracker.get_level_progress(level)
        total_words += progress.get("expected_total", 0)
        learned_words += progress.get("known", 0) + progress.get("mastered", 0)
        mastered_words += progress.get("mastered", 0)
        
        pct = progress.get("progress_percentage", 0)
        bar = "█" * int(pct / 10) + "░" * (10 - int(pct / 10))
        lines.append(f"L{level}: {bar} {pct:.0f}%")
    
    overall_pct = (learned_words / total_words * 100) if total_words > 0 else 0
    
    lines.insert(1, f"\n*{get_text('overall', lang)}: {overall_pct:.1f}%*")
    lines.insert(2, f"📚 {get_text('learned', lang)}: {learned_words}/{total_words}")
    lines.insert(3, f"⭐ {get_text('mastered', lang)}: {mastered_words}\n")
    
    await callback.message.edit_text(
        "\n".join(lines),
        parse_mode="Markdown",
        reply_markup=get_back_button("menu:4000words", lang)
    )
    await callback.answer()
