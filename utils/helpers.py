"""
Helper utilities for the bot
"""
import random
from typing import List
import config


def get_random_motivation() -> str:
    """Get a random motivation message"""
    return random.choice(config.MOTIVATION_MESSAGES)


def get_random_encouragement() -> str:
    """Get a random encouragement message"""
    return random.choice(config.ENCOURAGEMENT_MESSAGES)


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


def validate_word_input(word: str) -> tuple:
    """
    Validate word input
    Returns: (is_valid, error_message or None)
    """
    if not word or not word.strip():
        return False, "Word cannot be empty"
    
    if len(word) > 100:
        return False, "Word is too long (max 100 characters)"
    
    if not any(c.isalpha() for c in word):
        return False, "Word must contain at least one letter"
    
    return True, None


def validate_meaning_input(meaning: str) -> tuple:
    """
    Validate meaning input
    Returns: (is_valid, error_message or None)
    """
    if not meaning or not meaning.strip():
        return False, "Meaning cannot be empty"
    
    if len(meaning) > 500:
        return False, "Meaning is too long (max 500 characters)"
    
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
