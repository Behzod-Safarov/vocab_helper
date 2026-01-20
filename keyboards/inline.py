"""
Inline Keyboards Module
Contains all inline keyboard builders for the bot
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import List, Dict, Optional
import config


# ============ Main Menu Keyboards ============

def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """Main menu keyboard"""
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="📚 Learn", callback_data="menu:learn"),
        InlineKeyboardButton(text="📝 Test", callback_data="menu:test"),
    )
    builder.row(
        InlineKeyboardButton(text="🔄 Review", callback_data="menu:review"),
        InlineKeyboardButton(text="📊 Stats", callback_data="menu:stats"),
    )
    builder.row(
        InlineKeyboardButton(text="📘 4000 Words", callback_data="menu:4000words"),
    )
    builder.row(
        InlineKeyboardButton(text="⚙️ Settings", callback_data="menu:settings"),
    )
    
    return builder.as_markup()


def get_back_button(callback_data: str = "menu:main") -> InlineKeyboardMarkup:
    """Simple back button"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="◀️ Back", callback_data=callback_data)
    )
    return builder.as_markup()


# ============ Learn Section Keyboards ============

def get_learn_menu_keyboard() -> InlineKeyboardMarkup:
    """Learning options menu"""
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="📘 4000 Essential Words", callback_data="learn:4000"),
    )
    builder.row(
        InlineKeyboardButton(text="✏️ My Custom Words", callback_data="learn:custom"),
    )
    builder.row(
        InlineKeyboardButton(text="🔄 Review Due Words", callback_data="learn:review"),
    )
    builder.row(
        InlineKeyboardButton(text="➕ Add New Word", callback_data="learn:add"),
    )
    builder.row(
        InlineKeyboardButton(text="◀️ Main Menu", callback_data="menu:main"),
    )
    
    return builder.as_markup()


def get_level_selection_keyboard(for_action: str = "learn") -> InlineKeyboardMarkup:
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
                        text=f"📘 Level {level}",
                        callback_data=f"{for_action}:level:{level}"
                    )
                )
        builder.row(*row_buttons)
    
    builder.row(
        InlineKeyboardButton(text="◀️ Back", callback_data=f"menu:{for_action}")
    )
    
    return builder.as_markup()


def get_unit_selection_keyboard(
    level: int,
    for_action: str = "learn",
    page: int = 0,
    units_per_page: int = 10
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
                text="◀️ Prev",
                callback_data=f"{for_action}:level:{level}:page:{page-1}"
            )
        )
    
    total_pages = (config.UNITS_PER_LEVEL + units_per_page - 1) // units_per_page
    if page < total_pages - 1:
        nav_buttons.append(
            InlineKeyboardButton(
                text="Next ▶️",
                callback_data=f"{for_action}:level:{level}:page:{page+1}"
            )
        )
    
    if nav_buttons:
        builder.row(*nav_buttons)
    
    builder.row(
        InlineKeyboardButton(text="◀️ Back to Levels", callback_data=f"{for_action}:4000")
    )
    
    return builder.as_markup()


def get_word_learning_keyboard(word_id: str) -> InlineKeyboardMarkup:
    """Keyboard for learning a word"""
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="✅ I Know This", callback_data=f"learn:know:{word_id}"),
        InlineKeyboardButton(text="❌ I Don't Know", callback_data=f"learn:unknown:{word_id}"),
    )
    builder.row(
        InlineKeyboardButton(text="🔊 Pronunciation", callback_data=f"learn:audio:{word_id}"),
        InlineKeyboardButton(text="📝 Example", callback_data=f"learn:example:{word_id}"),
    )
    builder.row(
        InlineKeyboardButton(text="⏭ Next Word", callback_data=f"learn:next:{word_id}"),
    )
    builder.row(
        InlineKeyboardButton(text="◀️ Back", callback_data="learn:4000"),
    )
    
    return builder.as_markup()


def get_flashcard_keyboard(word_id: str) -> InlineKeyboardMarkup:
    """Keyboard for flashcard review"""
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="👁 Show Answer", callback_data=f"flash:show:{word_id}"),
    )
    builder.row(
        InlineKeyboardButton(text="◀️ End Session", callback_data="learn:menu"),
    )
    
    return builder.as_markup()


def get_flashcard_response_keyboard(word_id: str) -> InlineKeyboardMarkup:
    """Keyboard after showing flashcard answer"""
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="✅ I Remember", callback_data=f"flash:correct:{word_id}"),
        InlineKeyboardButton(text="❌ I Forgot", callback_data=f"flash:wrong:{word_id}"),
    )
    builder.row(
        InlineKeyboardButton(text="◀️ End Session", callback_data="learn:menu"),
    )
    
    return builder.as_markup()


# ============ Test Section Keyboards ============

def get_test_menu_keyboard() -> InlineKeyboardMarkup:
    """Test options menu"""
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="📝 Unit Test", callback_data="test:unit"),
    )
    builder.row(
        InlineKeyboardButton(text="📚 Level Test", callback_data="test:level"),
    )
    builder.row(
        InlineKeyboardButton(text="🔄 Review Test", callback_data="test:review"),
    )
    builder.row(
        InlineKeyboardButton(text="✏️ Custom Words Test", callback_data="test:custom"),
    )
    builder.row(
        InlineKeyboardButton(text="◀️ Main Menu", callback_data="menu:main"),
    )
    
    return builder.as_markup()


def get_quiz_answer_keyboard(
    options: List[str],
    question_id: str
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
        InlineKeyboardButton(text="💡 Hint", callback_data=f"quiz:hint:{question_id}"),
        InlineKeyboardButton(text="⏭ Skip", callback_data=f"quiz:skip:{question_id}"),
    )
    
    return builder.as_markup()


def get_quiz_continue_keyboard(is_correct: bool) -> InlineKeyboardMarkup:
    """Keyboard after answering a quiz question"""
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="➡️ Next Question", callback_data="quiz:next"),
    )
    builder.row(
        InlineKeyboardButton(text="🏁 End Test", callback_data="quiz:end"),
    )
    
    return builder.as_markup()


def get_test_result_keyboard() -> InlineKeyboardMarkup:
    """Keyboard after test completion"""
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="🔄 Retry Test", callback_data="test:retry"),
        InlineKeyboardButton(text="📊 View Details", callback_data="test:details"),
    )
    builder.row(
        InlineKeyboardButton(text="📝 New Test", callback_data="menu:test"),
    )
    builder.row(
        InlineKeyboardButton(text="◀️ Main Menu", callback_data="menu:main"),
    )
    
    return builder.as_markup()


# ============ Review Section Keyboards ============

def get_review_menu_keyboard(due_count: int = 0) -> InlineKeyboardMarkup:
    """Review options menu"""
    builder = InlineKeyboardBuilder()
    
    due_text = f"🔄 Start Review ({due_count} due)" if due_count > 0 else "🔄 Start Review"
    
    builder.row(
        InlineKeyboardButton(text=due_text, callback_data="review:start"),
    )
    builder.row(
        InlineKeyboardButton(text="⚠️ Weak Words", callback_data="review:weak"),
    )
    builder.row(
        InlineKeyboardButton(text="📅 Schedule", callback_data="review:schedule"),
    )
    builder.row(
        InlineKeyboardButton(text="◀️ Main Menu", callback_data="menu:main"),
    )
    
    return builder.as_markup()


# ============ Stats Section Keyboards ============

def get_stats_menu_keyboard() -> InlineKeyboardMarkup:
    """Statistics menu"""
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="📊 Overall Stats", callback_data="stats:overall"),
    )
    builder.row(
        InlineKeyboardButton(text="📘 Level Progress", callback_data="stats:levels"),
    )
    builder.row(
        InlineKeyboardButton(text="🔥 Streak Info", callback_data="stats:streak"),
    )
    builder.row(
        InlineKeyboardButton(text="⚠️ Weak Words", callback_data="stats:weak"),
    )
    builder.row(
        InlineKeyboardButton(text="◀️ Main Menu", callback_data="menu:main"),
    )
    
    return builder.as_markup()


def get_level_stats_keyboard() -> InlineKeyboardMarkup:
    """Level progress selection"""
    builder = InlineKeyboardBuilder()
    
    for i in range(0, config.LEVELS, 3):
        row_buttons = []
        for j in range(3):
            level = i + j + 1
            if level <= config.LEVELS:
                row_buttons.append(
                    InlineKeyboardButton(
                        text=f"Level {level}",
                        callback_data=f"stats:level:{level}"
                    )
                )
        builder.row(*row_buttons)
    
    builder.row(
        InlineKeyboardButton(text="◀️ Back", callback_data="menu:stats"),
    )
    
    return builder.as_markup()


# ============ Settings Keyboards ============

def get_settings_keyboard(settings: Dict) -> InlineKeyboardMarkup:
    """Settings menu"""
    builder = InlineKeyboardBuilder()
    
    notif_status = "🔔 On" if settings.get("notifications_enabled", True) else "🔕 Off"
    
    builder.row(
        InlineKeyboardButton(
            text=f"Notifications: {notif_status}",
            callback_data="settings:toggle_notif"
        ),
    )
    builder.row(
        InlineKeyboardButton(
            text=f"Daily Words: {settings.get('daily_new_words', 10)}",
            callback_data="settings:daily_words"
        ),
    )
    builder.row(
        InlineKeyboardButton(
            text=f"Review Words: {settings.get('daily_review_words', 20)}",
            callback_data="settings:review_words"
        ),
    )
    builder.row(
        InlineKeyboardButton(
            text=f"Reminder Time: {settings.get('notification_time', '09:00')}",
            callback_data="settings:reminder_time"
        ),
    )
    builder.row(
        InlineKeyboardButton(text="◀️ Main Menu", callback_data="menu:main"),
    )
    
    return builder.as_markup()


def get_number_selection_keyboard(
    callback_prefix: str,
    options: List[int],
    current: int = None
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
        InlineKeyboardButton(text="◀️ Back", callback_data="menu:settings"),
    )
    
    return builder.as_markup()


# ============ 4000 Words Keyboards ============

def get_4000_words_menu_keyboard() -> InlineKeyboardMarkup:
    """4000 Words main menu"""
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="📖 Browse Levels", callback_data="4000:browse"),
    )
    builder.row(
        InlineKeyboardButton(text="📚 Continue Learning", callback_data="4000:continue"),
    )
    builder.row(
        InlineKeyboardButton(text="📝 Take Test", callback_data="4000:test"),
    )
    builder.row(
        InlineKeyboardButton(text="📊 View Progress", callback_data="4000:progress"),
    )
    builder.row(
        InlineKeyboardButton(text="◀️ Main Menu", callback_data="menu:main"),
    )
    
    return builder.as_markup()


# ============ Custom Word Keyboards ============

def get_add_word_keyboard() -> InlineKeyboardMarkup:
    """Cancel adding word"""
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="❌ Cancel", callback_data="learn:menu"),
    )
    
    return builder.as_markup()


def get_confirm_keyboard(action: str, item_id: str) -> InlineKeyboardMarkup:
    """Confirmation keyboard"""
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(
            text="✅ Confirm",
            callback_data=f"confirm:{action}:{item_id}"
        ),
        InlineKeyboardButton(
            text="❌ Cancel",
            callback_data=f"cancel:{action}:{item_id}"
        ),
    )
    
    return builder.as_markup()
