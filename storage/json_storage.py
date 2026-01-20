"""
JSON-based storage system for user data and vocabulary
"""
import os
import json
import aiofiles
from datetime import datetime
from typing import Dict, List, Optional, Any
import config


async def ensure_directories():
    """Ensure all required directories exist"""
    directories = [
        config.DATA_DIR,
        config.USERS_DIR,
        config.WORDS_4000_DIR,
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)


def get_user_file_path(user_id: int) -> str:
    """Get the file path for a user's data"""
    return os.path.join(config.USERS_DIR, f"{user_id}.json")


def get_default_user_data(user_id: int, username: str = None) -> Dict:
    """Create default user data structure"""
    return {
        "user_id": user_id,
        "username": username,
        "created_at": datetime.now().isoformat(),
        "last_active": datetime.now().isoformat(),
        "settings": {
            "daily_new_words": config.DAILY_NEW_WORDS,
            "daily_review_words": config.DAILY_REVIEW_WORDS,
            "notifications_enabled": True,
            "notification_time": "09:00",
        },
        "stats": {
            "total_words_learned": 0,
            "total_reviews": 0,
            "total_tests_taken": 0,
            "correct_answers": 0,
            "wrong_answers": 0,
            "current_streak": 0,
            "longest_streak": 0,
            "last_study_date": None,
        },
        "custom_vocabulary": [],
        "words_4000_progress": {
            "current_level": 1,
            "current_unit": 1,
            "completed_units": [],
            "word_status": {},  # word_id: {status, reviews, last_review, next_review, ease_factor}
        },
        "review_queue": [],
        "learning_session": None,
        "test_session": None,
    }


async def load_user_data(user_id: int) -> Optional[Dict]:
    """Load user data from JSON file"""
    file_path = get_user_file_path(user_id)
    
    if not os.path.exists(file_path):
        return None
    
    try:
        async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
            content = await f.read()
            return json.loads(content)
    except (json.JSONDecodeError, IOError):
        return None


async def save_user_data(user_id: int, data: Dict) -> bool:
    """Save user data to JSON file"""
    await ensure_directories()
    file_path = get_user_file_path(user_id)
    
    try:
        data["last_active"] = datetime.now().isoformat()
        async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
            await f.write(json.dumps(data, indent=2, ensure_ascii=False))
        return True
    except IOError:
        return False


async def get_or_create_user(user_id: int, username: str = None) -> Dict:
    """Get existing user data or create new user"""
    data = await load_user_data(user_id)
    
    if data is None:
        data = get_default_user_data(user_id, username)
        await save_user_data(user_id, data)
    
    return data


async def update_user_field(user_id: int, field_path: str, value: Any) -> bool:
    """Update a specific field in user data using dot notation"""
    data = await load_user_data(user_id)
    
    if data is None:
        return False
    
    # Navigate to nested field
    keys = field_path.split('.')
    current = data
    
    for key in keys[:-1]:
        if key not in current:
            current[key] = {}
        current = current[key]
    
    current[keys[-1]] = value
    return await save_user_data(user_id, data)


async def load_4000_words_level(level: int) -> Optional[Dict]:
    """Load a specific level of 4000 words"""
    file_path = os.path.join(config.WORDS_4000_DIR, f"level_{level}.json")
    
    if not os.path.exists(file_path):
        return None
    
    try:
        async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
            content = await f.read()
            return json.loads(content)
    except (json.JSONDecodeError, IOError):
        return None


async def get_unit_words(level: int, unit: int) -> Optional[List[Dict]]:
    """Get words from a specific unit"""
    level_data = await load_4000_words_level(level)
    
    if level_data is None:
        return None
    
    unit_key = f"unit_{unit}"
    return level_data.get("units", {}).get(unit_key, {}).get("words", [])


async def get_all_words_in_level(level: int) -> List[Dict]:
    """Get all words from a level"""
    level_data = await load_4000_words_level(level)
    
    if level_data is None:
        return []
    
    all_words = []
    for unit_key, unit_data in level_data.get("units", {}).items():
        for word in unit_data.get("words", []):
            word["unit"] = int(unit_key.split("_")[1])
            word["level"] = level
            all_words.append(word)
    
    return all_words


class UserDataManager:
    """Manager class for user data operations"""
    
    def __init__(self, user_id: int):
        self.user_id = user_id
        self._data = None
    
    async def load(self) -> Dict:
        """Load user data"""
        self._data = await get_or_create_user(self.user_id)
        return self._data
    
    async def save(self) -> bool:
        """Save current user data"""
        if self._data is None:
            return False
        return await save_user_data(self.user_id, self._data)
    
    @property
    def data(self) -> Dict:
        return self._data
    
    async def add_custom_word(self, word_data: Dict) -> bool:
        """Add a custom word to user's vocabulary"""
        if self._data is None:
            await self.load()
        
        word_data["id"] = f"custom_{len(self._data['custom_vocabulary']) + 1}"
        word_data["added_at"] = datetime.now().isoformat()
        word_data["status"] = "new"
        word_data["reviews"] = 0
        word_data["correct_count"] = 0
        word_data["ease_factor"] = 2.5
        word_data["interval"] = 0
        word_data["next_review"] = datetime.now().isoformat()
        
        self._data["custom_vocabulary"].append(word_data)
        return await self.save()
    
    async def update_word_status(self, word_id: str, is_4000: bool, correct: bool) -> bool:
        """Update word status after review"""
        if self._data is None:
            await self.load()
        
        if is_4000:
            word_status = self._data["words_4000_progress"]["word_status"]
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
            
            status = word_status[word_id]
        else:
            # Find custom word
            status = None
            for word in self._data["custom_vocabulary"]:
                if word["id"] == word_id:
                    status = word
                    break
            
            if status is None:
                return False
        
        # Update status based on answer
        status["reviews"] += 1
        status["last_review"] = datetime.now().isoformat()
        
        if correct:
            status["correct_count"] += 1
            status["ease_factor"] = min(2.5, status["ease_factor"] + 0.1)
            
            if status["correct_count"] >= config.MASTERED_THRESHOLD:
                status["status"] = "mastered"
            elif status["correct_count"] >= config.WEAK_THRESHOLD:
                status["status"] = "known"
            else:
                status["status"] = "learning"
        else:
            status["correct_count"] = max(0, status["correct_count"] - 1)
            status["ease_factor"] = max(1.3, status["ease_factor"] - 0.2)
            status["status"] = "weak" if status["reviews"] > 1 else "learning"
        
        # Calculate next review using spaced repetition
        from modules.spaced_repetition import calculate_next_review
        status["interval"], status["next_review"] = calculate_next_review(
            status["interval"],
            status["ease_factor"],
            correct
        )
        
        return await self.save()
    
    async def update_stats(self, correct: bool, test_completed: bool = False):
        """Update user statistics"""
        if self._data is None:
            await self.load()
        
        stats = self._data["stats"]
        stats["total_reviews"] += 1
        
        if correct:
            stats["correct_answers"] += 1
        else:
            stats["wrong_answers"] += 1
        
        if test_completed:
            stats["total_tests_taken"] += 1
        
        # Update streak
        today = datetime.now().date().isoformat()
        last_study = stats.get("last_study_date")
        
        if last_study:
            last_date = datetime.fromisoformat(last_study).date()
            today_date = datetime.now().date()
            days_diff = (today_date - last_date).days
            
            if days_diff == 1:
                stats["current_streak"] += 1
            elif days_diff > 1:
                stats["current_streak"] = 1
        else:
            stats["current_streak"] = 1
        
        stats["longest_streak"] = max(stats["longest_streak"], stats["current_streak"])
        stats["last_study_date"] = today
        
        await self.save()
    
    async def get_words_due_for_review(self) -> List[Dict]:
        """Get words that are due for review"""
        if self._data is None:
            await self.load()
        
        now = datetime.now()
        due_words = []
        
        # Check 4000 words
        word_status = self._data["words_4000_progress"]["word_status"]
        for word_id, status in word_status.items():
            if status["next_review"]:
                next_review = datetime.fromisoformat(status["next_review"])
                if next_review <= now and status["status"] != "mastered":
                    due_words.append({
                        "word_id": word_id,
                        "is_4000": True,
                        "status": status,
                    })
        
        # Check custom vocabulary
        for word in self._data["custom_vocabulary"]:
            if word.get("next_review"):
                next_review = datetime.fromisoformat(word["next_review"])
                if next_review <= now and word.get("status") != "mastered":
                    due_words.append({
                        "word_id": word["id"],
                        "word_data": word,
                        "is_4000": False,
                        "status": word,
                    })
        
        return due_words
