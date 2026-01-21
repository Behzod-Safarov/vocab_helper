"""
Vocabulary management module
Handles word operations, searching, and management
"""
from typing import Dict, List, Optional
from datetime import datetime
from storage.json_storage import (
    UserDataManager,
    load_4000_words_level,
    get_unit_words,
    get_all_words_in_level,
)
import config


class VocabularyManager:
    """Manages vocabulary operations for a user"""
    
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.user_manager = UserDataManager(user_id)
    
    async def initialize(self):
        """Initialize the vocabulary manager"""
        await self.user_manager.load()
    
    async def add_custom_word(
        self,
        word: str,
        meaning: str,
        example: str = None,
        synonyms: List[str] = None,
        antonyms: List[str] = None,
        part_of_speech: str = None,
    ) -> Dict:
        """Add a custom word to user's vocabulary"""
        word_data = {
            "word": word.strip().lower(),
            "meaning": meaning.strip(),
            "example": example.strip() if example else None,
            "synonyms": synonyms or [],
            "antonyms": antonyms or [],
            "part_of_speech": part_of_speech,
        }
        
        await self.user_manager.add_custom_word(word_data)
        return word_data
    
    async def get_custom_words(self, status: str = None) -> List[Dict]:
        """Get user's custom vocabulary, optionally filtered by status"""
        data = await self.user_manager.load()
        words = data.get("custom_vocabulary", [])
        
        if status:
            words = [w for w in words if w.get("status") == status]
        
        return words
    
    async def search_custom_words(self, query: str) -> List[Dict]:
        """Search custom vocabulary by word or meaning"""
        data = await self.user_manager.load()
        words = data.get("custom_vocabulary", [])
        query = query.lower()
        
        results = []
        for word in words:
            if (query in word.get("word", "").lower() or 
                query in word.get("meaning", "").lower()):
                results.append(word)
        
        return results
    
    async def delete_custom_word(self, word_id: str) -> bool:
        """Delete a custom word"""
        data = await self.user_manager.load()
        words = data.get("custom_vocabulary", [])
        
        for i, word in enumerate(words):
            if word.get("id") == word_id:
                words.pop(i)
                await self.user_manager.save()
                return True
        
        return False
    
    async def get_4000_word(self, level: int, unit: int, word_index: int) -> Optional[Dict]:
        """Get a specific word from 4000 words"""
        words = await get_unit_words(level, unit)
        
        if words and 0 <= word_index < len(words):
            word = words[word_index]
            word["level"] = level
            word["unit"] = unit
            return word
        
        return None
    
    async def get_4000_unit_words(self, level: int, unit: int) -> List[Dict]:
        """Get all words from a specific unit"""
        words = await get_unit_words(level, unit)
        
        if words:
            for i, word in enumerate(words):
                word["level"] = level
                word["unit"] = unit
                word["index"] = i
        
        return words or []
    
    async def get_4000_level_words(self, level: int) -> List[Dict]:
        """Get all words from a level"""
        return await get_all_words_in_level(level)
    
    async def get_word_status(self, word_id: str, is_4000: bool = True) -> Optional[Dict]:
        """Get the learning status of a word"""
        data = await self.user_manager.load()
        
        if is_4000:
            return data["words_4000_progress"]["word_status"].get(word_id)
        else:
            for word in data.get("custom_vocabulary", []):
                if word.get("id") == word_id:
                    return {
                        "status": word.get("status", "new"),
                        "reviews": word.get("reviews", 0),
                        "correct_count": word.get("correct_count", 0),
                        "ease_factor": word.get("ease_factor", 2.5),
                        "interval": word.get("interval", 0),
                        "next_review": word.get("next_review"),
                    }
        
        return None
    
    async def mark_word_learned(self, word_id: str, is_4000: bool = True) -> bool:
        """Mark a word as learned (first exposure)"""
        data = await self.user_manager.load()
        
        if is_4000:
            word_status = data["words_4000_progress"]["word_status"]
            if word_id not in word_status:
                word_status[word_id] = {
                    "status": "learning",
                    "reviews": 0,
                    "correct_count": 0,
                    "ease_factor": 2.5,
                    "interval": 0,
                    "last_review": None,
                    "next_review": datetime.now().isoformat(),
                }
                data["stats"]["total_words_learned"] += 1
                await self.user_manager.save()
                return True
        
        return False
    
    async def get_user_progress_for_unit(self, level: int, unit: int) -> Dict:
        """Get user's progress for a specific unit"""
        words = await self.get_4000_unit_words(level, unit)
        data = await self.user_manager.load()
        word_status = data["words_4000_progress"]["word_status"]
        
        progress = {
            "total": len(words),
            "new": 0,
            "learning": 0,
            "known": 0,
            "mastered": 0,
            "weak": 0,
        }
        
        for word in words:
            word_id = f"L{level}U{unit}W{word.get('index', 0)}"
            status = word_status.get(word_id, {}).get("status", "new")
            progress[status] = progress.get(status, 0) + 1
        
        progress["completion_rate"] = (
            (progress["known"] + progress["mastered"]) / progress["total"] * 100
            if progress["total"] > 0 else 0
        )
        
        return progress
    
    async def get_user_progress_for_level(self, level: int) -> Dict:
        """Get user's progress for a specific level"""
        progress = {
            "total_words": 0,
            "learned": 0,
            "mastered": 0,
            "weak": 0,
            "units_completed": 0,
            "total_units": config.UNITS_PER_LEVEL,
        }
        
        for unit in range(1, config.UNITS_PER_LEVEL + 1):
            unit_progress = await self.get_user_progress_for_unit(level, unit)
            progress["total_words"] += unit_progress["total"]
            progress["learned"] += unit_progress["known"] + unit_progress["mastered"]
            progress["mastered"] += unit_progress["mastered"]
            progress["weak"] += unit_progress["weak"]
            
            if unit_progress["completion_rate"] >= 80:
                progress["units_completed"] += 1
        
        progress["completion_rate"] = (
            progress["learned"] / progress["total_words"] * 100
            if progress["total_words"] > 0 else 0
        )
        
        return progress
    
    async def get_weak_words(self, limit: int = 20) -> List[Dict]:
        """Get words marked as weak that need more practice"""
        data = await self.user_manager.load()
        weak_words = []
        
        # Get weak 4000 words
        word_status = data["words_4000_progress"]["word_status"]
        for word_id, status in word_status.items():
            if status.get("status") == "weak":
                # Parse word_id to get level, unit, word index
                parts = word_id.replace("L", "").replace("U", " ").replace("W", " ").split()
                if len(parts) == 3:
                    level, unit, idx = int(parts[0]), int(parts[1]), int(parts[2])
                    word = await self.get_4000_word(level, unit, idx)
                    if word:
                        word["word_id"] = word_id
                        word["is_4000"] = True
                        word["status_info"] = status
                        weak_words.append(word)
        
        # Get weak custom words
        for word in data.get("custom_vocabulary", []):
            if word.get("status") == "weak":
                word["is_4000"] = False
                weak_words.append(word)
        
        return weak_words[:limit]
    
    async def get_words_for_learning(self, count: int = 10) -> List[Dict]:
        """Get words for a learning session (mix of new and review)"""
        data = await self.user_manager.load()
        progress = data["words_4000_progress"]
        
        words_to_learn = []
        
        # Get next words from current level/unit
        current_level = progress.get("current_level", 1)
        current_unit = progress.get("current_unit", 1)
        
        unit_words = await self.get_4000_unit_words(current_level, current_unit)
        word_status = progress["word_status"]
        
        for i, word in enumerate(unit_words):
            word_id = f"L{current_level}U{current_unit}W{i}"
            status = word_status.get(word_id, {}).get("status", "new")
            
            if status == "new" and len(words_to_learn) < count:
                word["word_id"] = word_id
                word["is_4000"] = True
                words_to_learn.append(word)
        
        return words_to_learn


def format_word_for_display(
    word: Dict, 
    show_answer: bool = False, 
    lang: str = "en",
    translation_lang: str = "both"
) -> str:
    """
    Format a word for display in Telegram
    
    Args:
        word: Word dictionary with word data
        show_answer: Whether to show the meaning
        lang: Interface language (en, uz, ru)
        translation_lang: Translation to show (both, uz, ru, none)
    """
    from locales import get_text
    
    lines = []
    
    lines.append(f"📚 *{word.get('word', 'Unknown')}*")
    
    if word.get("part_of_speech"):
        lines.append(f"_{word['part_of_speech']}_")
    
    if show_answer or word.get("show_meaning", True):
        # English meaning
        lines.append(f"\n{get_text('meaning_label', lang)} {word.get('meaning', 'N/A')}")
        
        # Translations based on user setting
        if translation_lang in ["both", "uz"] and word.get("meaningUz"):
            lines.append(f"{get_text('meaning_uz_label', lang)} {word['meaningUz']}")
        
        if translation_lang in ["both", "ru"] and word.get("meaningRu"):
            lines.append(f"{get_text('meaning_ru_label', lang)} {word['meaningRu']}")
    
    if word.get("example"):
        lines.append(f"\n{get_text('example_label', lang)} _{word['example']}_")
    
    if word.get("synonyms"):
        synonyms = ", ".join(word["synonyms"][:3])
        lines.append(f"\n{get_text('synonyms_label', lang)} {synonyms}")
    
    if word.get("antonyms"):
        antonyms = ", ".join(word["antonyms"][:3])
        lines.append(f"\n↔️ *Antonyms:* {antonyms}")
    
    if word.get("level") and word.get("unit"):
        lines.append(f"\n📍 Level {word['level']} • Unit {word['unit']}")
    
    return "\n".join(lines)


def format_word_card(word: Dict, lang: str = "en") -> str:
    """Format word as a flashcard (word only, no meaning)"""
    lines = [
        f"📚 *{word.get('word', 'Unknown')}*",
    ]
    
    if word.get("part_of_speech"):
        lines.append(f"_{word['part_of_speech']}_")
    
    prompts = {
        "en": "\n🤔 Do you remember this word?",
        "uz": "\n🤔 Bu so'zni eslaysizmi?",
        "ru": "\n🤔 Вы помните это слово?"
    }
    lines.append(prompts.get(lang, prompts["en"]))
    
    return "\n".join(lines)
