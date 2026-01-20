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
import config

router = Router()


@router.message(Command("4000words"))
async def cmd_4000words(message: Message):
    """Handle /4000words command"""
    await message.answer(
        "📘 *4000 Essential English Words*\n\n"
        "Master vocabulary across 6 levels, from beginner to advanced.\n\n"
        "• 6 Levels\n"
        "• 30 Units per level\n"
        "• ~20 Words per unit\n\n"
        "What would you like to do?",
        parse_mode="Markdown",
        reply_markup=get_4000_words_menu_keyboard()
    )


@router.callback_query(F.data == "menu:4000words")
async def show_4000_menu(callback: CallbackQuery):
    """Show 4000 words menu"""
    await callback.message.edit_text(
        "📘 *4000 Essential English Words*\n\n"
        "What would you like to do?",
        parse_mode="Markdown",
        reply_markup=get_4000_words_menu_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "4000:browse")
async def browse_levels(callback: CallbackQuery):
    """Browse all levels"""
    user_id = callback.from_user.id
    
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    
    tracker = ProgressTracker(user_manager.data)
    
    # Build level overview
    lines = ["📘 *4000 Essential Words*\n"]
    
    for level in range(1, config.LEVELS + 1):
        progress = tracker.get_level_progress(level)
        pct = progress.get("progress_percentage", 0)
        
        # Progress bar
        filled = int(pct / 10)
        bar = "█" * filled + "░" * (10 - filled)
        
        desc = get_level_description(level)
        lines.append(f"*Level {level}*: {bar} {pct:.0f}%")
        lines.append(f"_{desc}_\n")
    
    await callback.message.edit_text(
        "\n".join(lines),
        parse_mode="Markdown",
        reply_markup=get_level_selection_keyboard("browse")
    )
    await callback.answer()


@router.callback_query(F.data.startswith("browse:level:"))
async def browse_level_units(callback: CallbackQuery):
    """Browse units in a level"""
    parts = callback.data.split(":")
    level = int(parts[2])
    page = int(parts[4]) if len(parts) > 4 and parts[3] == "page" else 0
    
    user_id = callback.from_user.id
    
    vocab_manager = VocabularyManager(user_id)
    await vocab_manager.initialize()
    
    # Get level progress
    progress = await vocab_manager.get_user_progress_for_level(level)
    
    desc = get_level_description(level)
    
    await callback.message.edit_text(
        f"📘 *Level {level}*\n"
        f"_{desc}_\n\n"
        f"📊 Progress: {progress['completion_rate']:.1f}%\n"
        f"✅ Learned: {progress['learned']}/{progress['total_words']}\n"
        f"⭐ Mastered: {progress['mastered']}\n"
        f"⚠️ Weak: {progress['weak']}\n\n"
        f"Select a unit:",
        parse_mode="Markdown",
        reply_markup=get_unit_selection_keyboard(level, "browse", page)
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
    
    vocab_manager = VocabularyManager(user_id)
    await vocab_manager.initialize()
    
    # Get unit words
    words = await vocab_manager.get_4000_unit_words(level, unit)
    
    if not words:
        await callback.message.edit_text(
            f"❌ No words found for Level {level} Unit {unit}.\n\n"
            "The word data may not be loaded yet.",
            reply_markup=get_back_button(f"browse:level:{level}")
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
        word_list.append(f"...and {len(words) - 10} more")
    
    await callback.message.edit_text(
        f"📗 *Level {level} • Unit {unit}*\n\n"
        f"📊 Progress: {progress['completion_rate']:.1f}%\n"
        f"📚 Words: {progress['total']}\n"
        f"✅ Known: {progress['known']}\n"
        f"⭐ Mastered: {progress['mastered']}\n\n"
        f"*Words in this unit:*\n"
        + "\n".join(word_list),
        parse_mode="Markdown",
        reply_markup=get_back_button(f"browse:level:{level}")
    )
    await callback.answer()


@router.callback_query(F.data == "4000:continue")
async def continue_learning(callback: CallbackQuery):
    """Continue learning from where user left off"""
    user_id = callback.from_user.id
    
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    
    progress = user_manager.data.get("words_4000_progress", {})
    current_level = progress.get("current_level", 1)
    current_unit = progress.get("current_unit", 1)
    
    await callback.message.edit_text(
        f"📖 *Continue Learning*\n\n"
        f"You're currently on:\n"
        f"📘 Level {current_level} • Unit {current_unit}\n\n"
        f"Ready to continue?",
        parse_mode="Markdown",
        reply_markup=get_back_button(f"learn:L{current_level}U{current_unit}")
    )
    await callback.answer()


@router.callback_query(F.data == "4000:test")
async def test_4000(callback: CallbackQuery):
    """Redirect to test menu for 4000 words"""
    from keyboards.inline import get_test_menu_keyboard
    
    await callback.message.edit_text(
        "📝 *4000 Words Test*\n\nChoose a test type:",
        parse_mode="Markdown",
        reply_markup=get_test_menu_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "4000:progress")
async def show_4000_progress(callback: CallbackQuery):
    """Show overall 4000 words progress"""
    user_id = callback.from_user.id
    
    user_manager = UserDataManager(user_id)
    await user_manager.load()
    
    tracker = ProgressTracker(user_manager.data)
    
    # Calculate overall progress
    total_words = 0
    learned_words = 0
    mastered_words = 0
    
    lines = ["📊 *4000 Words Progress*\n"]
    
    for level in range(1, config.LEVELS + 1):
        progress = tracker.get_level_progress(level)
        total_words += progress.get("expected_total", 0)
        learned_words += progress.get("known", 0) + progress.get("mastered", 0)
        mastered_words += progress.get("mastered", 0)
        
        pct = progress.get("progress_percentage", 0)
        bar = "█" * int(pct / 10) + "░" * (10 - int(pct / 10))
        lines.append(f"L{level}: {bar} {pct:.0f}%")
    
    overall_pct = (learned_words / total_words * 100) if total_words > 0 else 0
    
    lines.insert(1, f"\n*Overall: {overall_pct:.1f}%*")
    lines.insert(2, f"📚 Learned: {learned_words}/{total_words}")
    lines.insert(3, f"⭐ Mastered: {mastered_words}\n")
    
    await callback.message.edit_text(
        "\n".join(lines),
        parse_mode="Markdown",
        reply_markup=get_back_button("menu:4000words")
    )
    await callback.answer()
