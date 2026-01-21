"""
Inline Keyboards Module
Contains all inline keyboard builders for the bot
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import List, Dict, Optional
import config
from locales import get_text, LANGUAGES


# ============ Main Menu Keyboards ============

def get_main_menu_keyboard(lang: str = "en") -> InlineKeyboardMarkup:
    """Main menu keyboard"""
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text=get_text("btn_learn", lang), callback_data="menu:learn"),
        InlineKeyboardButton(text=get_text("btn_test", lang), callback_data="menu:test"),
    )
    builder.row(
        InlineKeyboardButton(text=get_text("btn_review", lang), callback_data="menu:review"),
        InlineKeyboardButton(text=get_text("btn_stats", lang), callback_data="menu:stats"),
    )
    builder.row(
        InlineKeyboardButton(text=get_text("btn_4000words", lang), callback_data="menu:4000words"),
    )
    builder.row(
        InlineKeyboardButton(text=get_text("btn_settings", lang), callback_data="menu:settings"),
    )
    
    return builder.as_markup()


def get_back_button(callback_data: str = "menu:main", lang: str = "en") -> InlineKeyboardMarkup:
    """Simple back button"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text=get_text("btn_back", lang), callback_data=callback_data)
    )
    return builder.as_markup()


# ============ Learn Section Keyboards ============

def get_learn_menu_keyboard(lang: str = "en") -> InlineKeyboardMarkup:
    """Learning options menu"""
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text=get_text("btn_4000_essential", lang), callback_data="learn:4000"),
    )
    builder.row(
        InlineKeyboardButton(text=get_text("btn_my_custom_words", lang), callback_data="learn:custom"),
    )
    builder.row(
        InlineKeyboardButton(text=get_text("btn_review_due", lang), callback_data="learn:review"),
    )
    builder.row(
        InlineKeyboardButton(text=get_text("btn_add_word", lang), callback_data="learn:add"),
    )
    builder.row(
        InlineKeyboardButton(text=get_text("btn_main_menu", lang), callback_data="menu:main"),
    )
    
    return builder.as_markup()


def get_level_selection_keyboard(for_action: str = "learn", lang: str = "en") -> InlineKeyboardMarkup:
    """Level selection keyboard (1-6)"""
    builder = InlineKeyboardBuilder()
    
    # Two levels per row
    for i in range(0, config.LEVELS, 2):
        row_buttons = []
        for j in range(2):
            level = i + j + 1
            if level <= config.LEVELS:
                row_buttons.append(
                    InlineKeyboardButton(
                        text=f"📘 {get_text('level', lang)} {level}",
                        callback_data=f"{for_action}:level:{level}"
                    )
                )
        builder.row(*row_buttons)
    
    builder.row(
        InlineKeyboardButton(text=get_text("btn_back", lang), callback_data=f"menu:{for_action}")
    )
    
    return builder.as_markup()


def get_unit_selection_keyboard(
    level: int,
    for_action: str = "learn",
    page: int = 0,
    units_per_page: int = 10,
    lang: str = "en"
) -> InlineKeyboardMarkup:
    """Unit selection keyboard with pagination"""
    builder = InlineKeyboardBuilder()
    
    start_unit = page * units_per_page + 1
    end_unit = min(start_unit + units_per_page, config.UNITS_PER_LEVEL + 1)
    
    # Units in rows of 5
    for i in range(start_unit, end_unit, 5):
        row_buttons = []
        for j in range(5):
            unit = i + j
            if unit <= config.UNITS_PER_LEVEL:
                row_buttons.append(
                    InlineKeyboardButton(
                        text=f"{unit}",
                        callback_data=f"{for_action}:L{level}U{unit}"
                    )
                )
        builder.row(*row_buttons)
    
    # Pagination
    nav_buttons = []
    if page > 0:
        nav_buttons.append(
            InlineKeyboardButton(
                text=get_text("btn_prev_page", lang),
                callback_data=f"{for_action}:level:{level}:page:{page-1}"
            )
        )
    
    total_pages = (config.UNITS_PER_LEVEL + units_per_page - 1) // units_per_page
    if page < total_pages - 1:
        nav_buttons.append(
            InlineKeyboardButton(
                text=get_text("btn_next_page", lang),
                callback_data=f"{for_action}:level:{level}:page:{page+1}"
            )
        )
    
    if nav_buttons:
        builder.row(*nav_buttons)
    
    builder.row(
        InlineKeyboardButton(text=get_text("btn_back_to_levels", lang), callback_data=f"{for_action}:4000")
    )
    
    return builder.as_markup()


def get_word_learning_keyboard(word_id: str, lang: str = "en") -> InlineKeyboardMarkup:
    """Keyboard for learning a word"""
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text=get_text("btn_i_know", lang), callback_data=f"learn:know:{word_id}"),
        InlineKeyboardButton(text=get_text("btn_i_dont_know", lang), callback_data=f"learn:unknown:{word_id}"),
    )
    builder.row(
        InlineKeyboardButton(text=get_text("btn_pronunciation", lang), callback_data=f"learn:audio:{word_id}"),
        InlineKeyboardButton(text=get_text("btn_example", lang), callback_data=f"learn:example:{word_id}"),
    )
    builder.row(
        InlineKeyboardButton(text=get_text("btn_next_word", lang), callback_data=f"learn:next:{word_id}"),
    )
    builder.row(
        InlineKeyboardButton(text=get_text("btn_back", lang), callback_data="learn:4000"),
    )
    
    return builder.as_markup()


def get_flashcard_keyboard(word_id: str, lang: str = "en") -> InlineKeyboardMarkup:
    """Keyboard for flashcard review"""
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text=get_text("btn_show_answer", lang), callback_data=f"flash:show:{word_id}"),
    )
    builder.row(
        InlineKeyboardButton(text=get_text("btn_end_session", lang), callback_data="learn:menu"),
    )
    
    return builder.as_markup()


def get_flashcard_response_keyboard(word_id: str, lang: str = "en") -> InlineKeyboardMarkup:
    """Keyboard after showing flashcard answer"""
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text=get_text("btn_i_remember", lang), callback_data=f"flash:correct:{word_id}"),
        InlineKeyboardButton(text=get_text("btn_i_forgot", lang), callback_data=f"flash:wrong:{word_id}"),
    )
    builder.row(
        InlineKeyboardButton(text=get_text("btn_end_session", lang), callback_data="learn:menu"),
    )
    
    return builder.as_markup()


# ============ Test Section Keyboards ============

def get_test_menu_keyboard(lang: str = "en") -> InlineKeyboardMarkup:
    """Test options menu"""
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text=get_text("btn_unit_test", lang), callback_data="test:unit"),
    )
    builder.row(
        InlineKeyboardButton(text=get_text("btn_level_test_menu", lang), callback_data="test:level"),
    )
    builder.row(
        InlineKeyboardButton(text=get_text("btn_review_test", lang), callback_data="test:review"),
    )
    builder.row(
        InlineKeyboardButton(text=get_text("btn_custom_test", lang), callback_data="test:custom"),
    )
    builder.row(
        InlineKeyboardButton(text=get_text("btn_main_menu", lang), callback_data="menu:main"),
    )
    
    return builder.as_markup()


def get_quiz_answer_keyboard(
    options: List[str],
    question_id: str,
    lang: str = "en"
) -> InlineKeyboardMarkup:
    """Multiple choice answer keyboard"""
    builder = InlineKeyboardBuilder()
    
    letters = ["A", "B", "C", "D", "E", "F"]
    
    for i, option in enumerate(options):
        builder.row(
            InlineKeyboardButton(
                text=f"{letters[i]}. {option[:50]}",
                callback_data=f"quiz:ans:{question_id}:{i}"
            )
        )
    
    builder.row(
        InlineKeyboardButton(text=get_text("btn_hint", lang), callback_data=f"quiz:hint:{question_id}"),
        InlineKeyboardButton(text=get_text("btn_skip", lang), callback_data=f"quiz:skip:{question_id}"),
    )
    
    return builder.as_markup()


def get_quiz_continue_keyboard(is_correct: bool, lang: str = "en") -> InlineKeyboardMarkup:
    """Keyboard after answering a quiz question"""
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text=get_text("btn_next_question", lang), callback_data="quiz:next"),
    )
    builder.row(
        InlineKeyboardButton(text=get_text("btn_end_test", lang), callback_data="quiz:end"),
    )
    
    return builder.as_markup()


def get_test_result_keyboard(lang: str = "en") -> InlineKeyboardMarkup:
    """Keyboard after test completion"""
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text=get_text("btn_retry_test", lang), callback_data="test:retry"),
        InlineKeyboardButton(text=get_text("btn_view_details", lang), callback_data="test:details"),
    )
    builder.row(
        InlineKeyboardButton(text=get_text("btn_new_test", lang), callback_data="menu:test"),
    )
    builder.row(
        InlineKeyboardButton(text=get_text("btn_main_menu", lang), callback_data="menu:main"),
    )
    
    return builder.as_markup()


# ============ Review Section Keyboards ============

def get_review_menu_keyboard(due_count: int = 0, lang: str = "en") -> InlineKeyboardMarkup:
    """Review options menu"""
    builder = InlineKeyboardBuilder()
    
    if due_count > 0:
        due_text = get_text("btn_start_review_due", lang).format(count=due_count)
    else:
        due_text = get_text("btn_start_review", lang)
    
    builder.row(
        InlineKeyboardButton(text=due_text, callback_data="review:start"),
    )
    builder.row(
        InlineKeyboardButton(text=get_text("btn_review_weak", lang), callback_data="review:weak"),
    )
    builder.row(
        InlineKeyboardButton(text=get_text("btn_schedule", lang), callback_data="review:schedule"),
    )
    builder.row(
        InlineKeyboardButton(text=get_text("btn_main_menu", lang), callback_data="menu:main"),
    )
    
    return builder.as_markup()


# ============ Stats Section Keyboards ============

def get_stats_menu_keyboard(lang: str = "en") -> InlineKeyboardMarkup:
    """Statistics menu"""
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text=get_text("btn_overall_stats", lang), callback_data="stats:overall"),
    )
    builder.row(
        InlineKeyboardButton(text=get_text("btn_level_progress", lang), callback_data="stats:levels"),
    )
    builder.row(
        InlineKeyboardButton(text=get_text("btn_streak_info", lang), callback_data="stats:streak"),
    )
    builder.row(
        InlineKeyboardButton(text=get_text("btn_weak_words_stats", lang), callback_data="stats:weak"),
    )
    builder.row(
        InlineKeyboardButton(text=get_text("btn_main_menu", lang), callback_data="menu:main"),
    )
    
    return builder.as_markup()


def get_level_stats_keyboard(lang: str = "en") -> InlineKeyboardMarkup:
    """Level progress selection"""
    builder = InlineKeyboardBuilder()
    
    for i in range(0, config.LEVELS, 3):
        row_buttons = []
        for j in range(3):
            level = i + j + 1
            if level <= config.LEVELS:
                row_buttons.append(
                    InlineKeyboardButton(
                        text=f"{get_text('level', lang)} {level}",
                        callback_data=f"stats:level:{level}"
                    )
                )
        builder.row(*row_buttons)
    
    builder.row(
        InlineKeyboardButton(text=get_text("btn_back", lang), callback_data="menu:stats"),
    )
    
    return builder.as_markup()


# ============ Settings Keyboards ============

def get_settings_keyboard(settings: Dict, lang: str = "en") -> InlineKeyboardMarkup:
    """Settings menu"""
    builder = InlineKeyboardBuilder()
    
    # Language settings
    current_lang = settings.get("language", "en")
    lang_display = {"en": "🇬🇧 English", "uz": "🇺🇿 O'zbekcha", "ru": "🇷🇺 Русский"}.get(current_lang, "🇬🇧 English")
    builder.row(
        InlineKeyboardButton(
            text=f"{get_text('btn_language', lang)}: {lang_display}",
            callback_data="settings:language"
        ),
    )
    
    # Translation language
    trans_lang = settings.get("translation_language", "both")
    trans_display = {"both": "🌍 Both", "uz": "🇺🇿 Uzbek", "ru": "🇷🇺 Russian", "none": "🇬🇧 None"}.get(trans_lang, "🌍 Both")
    builder.row(
        InlineKeyboardButton(
            text=f"{get_text('btn_translation_lang', lang)}: {trans_display}",
            callback_data="settings:translation"
        ),
    )
    
    notif_status = get_text("notifications_on", lang) if settings.get("notifications_enabled", True) else get_text("notifications_off", lang)
    builder.row(
        InlineKeyboardButton(
            text=f"{get_text('btn_notifications', lang)}: {notif_status}",
            callback_data="settings:toggle_notif"
        ),
    )
    builder.row(
        InlineKeyboardButton(
            text=f"{get_text('btn_daily_words', lang)}: {settings.get('daily_new_words', 10)}",
            callback_data="settings:daily_words"
        ),
    )
    builder.row(
        InlineKeyboardButton(
            text=f"{get_text('btn_review_words', lang)}: {settings.get('daily_review_words', 20)}",
            callback_data="settings:review_words"
        ),
    )
    builder.row(
        InlineKeyboardButton(
            text=f"{get_text('btn_reminder_time', lang)}: {settings.get('notification_time', '09:00')}",
            callback_data="settings:reminder_time"
        ),
    )
    builder.row(
        InlineKeyboardButton(text=get_text("btn_main_menu", lang), callback_data="menu:main"),
    )
    
    return builder.as_markup()


def get_language_selection_keyboard(current_lang: str = "en") -> InlineKeyboardMarkup:
    """Language selection keyboard"""
    builder = InlineKeyboardBuilder()
    
    for code, name in LANGUAGES.items():
        marker = "✅ " if code == current_lang else ""
        builder.row(
            InlineKeyboardButton(
                text=f"{marker}{name}",
                callback_data=f"settings:setlang:{code}"
            )
        )
    
    builder.row(
        InlineKeyboardButton(text=get_text("btn_back", current_lang), callback_data="menu:settings"),
    )
    
    return builder.as_markup()


def get_translation_selection_keyboard(current: str = "both", lang: str = "en") -> InlineKeyboardMarkup:
    """Translation language selection keyboard"""
    builder = InlineKeyboardBuilder()
    
    options = [
        ("both", get_text("translation_both", lang)),
        ("uz", get_text("translation_uz", lang)),
        ("ru", get_text("translation_ru", lang)),
        ("none", get_text("translation_none", lang)),
    ]
    
    for code, name in options:
        marker = "✅ " if code == current else ""
        builder.row(
            InlineKeyboardButton(
                text=f"{marker}{name}",
                callback_data=f"settings:settrans:{code}"
            )
        )
    
    builder.row(
        InlineKeyboardButton(text=get_text("btn_back", lang), callback_data="menu:settings"),
    )
    
    return builder.as_markup()


def get_number_selection_keyboard(
    callback_prefix: str,
    options: List[int],
    current: int = None,
    lang: str = "en"
) -> InlineKeyboardMarkup:
    """Number selection keyboard for settings"""
    builder = InlineKeyboardBuilder()
    
    # 4 options per row
    for i in range(0, len(options), 4):
        row_buttons = []
        for j in range(4):
            if i + j < len(options):
                num = options[i + j]
                text = f"• {num} •" if num == current else str(num)
                row_buttons.append(
                    InlineKeyboardButton(
                        text=text,
                        callback_data=f"{callback_prefix}:{num}"
                    )
                )
        builder.row(*row_buttons)
    
    builder.row(
        InlineKeyboardButton(text=get_text("btn_back", lang), callback_data="menu:settings"),
    )
    
    return builder.as_markup()


# ============ 4000 Words Keyboards ============

def get_4000_words_menu_keyboard(lang: str = "en") -> InlineKeyboardMarkup:
    """4000 Words main menu"""
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text=get_text("btn_browse_levels", lang), callback_data="4000:browse"),
    )
    builder.row(
        InlineKeyboardButton(text=get_text("btn_continue_learning", lang), callback_data="4000:continue"),
    )
    builder.row(
        InlineKeyboardButton(text=get_text("btn_take_test", lang), callback_data="4000:test"),
    )
    builder.row(
        InlineKeyboardButton(text=get_text("btn_my_progress", lang), callback_data="4000:progress"),
    )
    builder.row(
        InlineKeyboardButton(text=get_text("btn_main_menu", lang), callback_data="menu:main"),
    )
    
    return builder.as_markup()


# ============ Custom Word Keyboards ============

def get_add_word_keyboard(lang: str = "en") -> InlineKeyboardMarkup:
    """Cancel adding word"""
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text=get_text("btn_cancel", lang), callback_data="learn:menu"),
    )
    
    return builder.as_markup()


def get_confirm_keyboard(action: str, item_id: str, lang: str = "en") -> InlineKeyboardMarkup:
    """Confirmation keyboard"""
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(
            text=get_text("btn_confirm", lang),
            callback_data=f"confirm:{action}:{item_id}"
        ),
        InlineKeyboardButton(
            text=get_text("btn_cancel", lang),
            callback_data=f"cancel:{action}:{item_id}"
        ),
    )
    
    return builder.as_markup()
