"""
Helper utilities for the bot
"""
import random
from typing import List, Optional
import config
from locales import get_text
from aiogram.types import Message, InlineKeyboardMarkup
from aiogram.exceptions import TelegramBadRequest


async def safe_edit_text(
    message: Message,
    text: str,
    parse_mode: Optional[str] = None,
    reply_markup: Optional[InlineKeyboardMarkup] = None
) -> bool:
    """
    Safely edit a message, ignoring 'message is not modified' errors.
    Returns True if edit was successful, False if message was unchanged.
    """
    try:
        await message.edit_text(text, parse_mode=parse_mode, reply_markup=reply_markup)
        return True
    except TelegramBadRequest as e:
        if "message is not modified" in str(e):
            return False
        raise


def get_random_motivation(lang: str = "en") -> str:
    """Get a random motivation message in the specified language"""
    motivation_keys = ["motivation_1", "motivation_2", "motivation_3", "motivation_4", "motivation_5"]
    return get_text(random.choice(motivation_keys), lang)


def get_random_encouragement(lang: str = "en") -> str:
    """Get a random encouragement message in the specified language"""
    encouragement_keys = ["encouragement_1", "encouragement_2", "encouragement_3", "encouragement_4", "encouragement_5"]
    return get_text(random.choice(encouragement_keys), lang)


def truncate_text(text: str, max_length: int = 200) -> str:
    """Truncate text to a maximum length"""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def format_time(seconds: int) -> str:
    """Format seconds to a human-readable time string"""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes}m {secs}s"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}h {minutes}m"


def parse_word_id(word_id: str) -> dict:
    """
    Parse a word ID like 'L1U5W3' into components
    Returns: {'level': 1, 'unit': 5, 'word_index': 3}
    """
    try:
        parts = word_id.replace("L", "").replace("U", " ").replace("W", " ").split()
        if len(parts) == 3:
            return {
                "level": int(parts[0]),
                "unit": int(parts[1]),
                "word_index": int(parts[2]),
            }
    except (ValueError, IndexError):
        pass
    return None


def create_word_id(level: int, unit: int, word_index: int) -> str:
    """Create a word ID from components"""
    return f"L{level}U{unit}W{word_index}"


def escape_markdown(text: str) -> str:
    """Escape special characters for Telegram MarkdownV2"""
    special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in special_chars:
        text = text.replace(char, f'\\{char}')
    return text


def safe_markdown(text: str) -> str:
    """Make text safe for Markdown (basic)"""
    # For basic Markdown mode, we only need to escape certain chars inside formatting
    return text.replace('_', '\\_').replace('*', '\\*').replace('`', '\\`').replace('[', '\\[')


# Validation error messages
VALIDATION_ERRORS = {
    "word_empty": {
        "en": "Word cannot be empty",
        "uz": "So'z bo'sh bo'lishi mumkin emas",
        "ru": "Слово не может быть пустым",
    },
    "word_too_long": {
        "en": "Word is too long (max 100 characters)",
        "uz": "So'z juda uzun (maksimum 100 belgi)",
        "ru": "Слово слишком длинное (макс. 100 символов)",
    },
    "word_no_letters": {
        "en": "Word must contain at least one letter",
        "uz": "So'zda kamida bitta harf bo'lishi kerak",
        "ru": "Слово должно содержать хотя бы одну букву",
    },
    "meaning_empty": {
        "en": "Meaning cannot be empty",
        "uz": "Ma'no bo'sh bo'lishi mumkin emas",
        "ru": "Значение не может быть пустым",
    },
    "meaning_too_long": {
        "en": "Meaning is too long (max 500 characters)",
        "uz": "Ma'no juda uzun (maksimum 500 belgi)",
        "ru": "Значение слишком длинное (макс. 500 символов)",
    },
}


def validate_word_input(word: str, lang: str = "en") -> tuple:
    """
    Validate word input
    Returns: (is_valid, error_message or None)
    """
    if not word or not word.strip():
        return False, VALIDATION_ERRORS["word_empty"].get(lang, VALIDATION_ERRORS["word_empty"]["en"])
    
    if len(word) > 100:
        return False, VALIDATION_ERRORS["word_too_long"].get(lang, VALIDATION_ERRORS["word_too_long"]["en"])
    
    if not any(c.isalpha() for c in word):
        return False, VALIDATION_ERRORS["word_no_letters"].get(lang, VALIDATION_ERRORS["word_no_letters"]["en"])
    
    return True, None


def validate_meaning_input(meaning: str, lang: str = "en") -> tuple:
    """
    Validate meaning input
    Returns: (is_valid, error_message or None)
    """
    if not meaning or not meaning.strip():
        return False, VALIDATION_ERRORS["meaning_empty"].get(lang, VALIDATION_ERRORS["meaning_empty"]["en"])
    
    if len(meaning) > 500:
        return False, VALIDATION_ERRORS["meaning_too_long"].get(lang, VALIDATION_ERRORS["meaning_too_long"]["en"])
    
    return True, None


def chunk_list(lst: List, chunk_size: int) -> List[List]:
    """Split a list into chunks of specified size"""
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def ordinal(n: int) -> str:
    """Convert a number to its ordinal representation"""
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    else:
        suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    return f"{n}{suffix}"


def format_list_items(items: List[str], max_items: int = 5) -> str:
    """Format a list of items with proper grammar"""
    if not items:
        return "none"
    
    if len(items) == 1:
        return items[0]
    
    if len(items) <= max_items:
        return ", ".join(items[:-1]) + f" and {items[-1]}"
    
    return ", ".join(items[:max_items]) + f" and {len(items) - max_items} more"


def calculate_score_emoji(percentage: float) -> str:
    """Get an emoji based on score percentage"""
    if percentage >= 90:
        return "🏆"
    elif percentage >= 80:
        return "⭐"
    elif percentage >= 70:
        return "✅"
    elif percentage >= 50:
        return "💪"
    else:
        return "📚"


def get_level_description(level: int) -> str:
    """Get description for each level"""
    descriptions = {
        1: "Beginner - Basic everyday words",
        2: "Elementary - Common vocabulary",
        3: "Pre-Intermediate - Expanding vocabulary",
        4: "Intermediate - Academic and practical",
        5: "Upper-Intermediate - Advanced concepts",
        6: "Advanced - Sophisticated vocabulary",
    }
    return descriptions.get(level, f"Level {level}")
