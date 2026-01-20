"""
Spaced Repetition System (SM-2 Algorithm)
Handles scheduling of word reviews based on user performance
"""
from datetime import datetime, timedelta
from typing import Tuple
import config


def calculate_next_review(
    current_interval: int,
    ease_factor: float,
    correct: bool,
    quality: int = None
) -> Tuple[int, str]:
    """
    Calculate the next review interval using SM-2 algorithm
    
    Args:
        current_interval: Current interval in days
        ease_factor: Current ease factor (1.3 - 2.5)
        correct: Whether the answer was correct
        quality: Quality of response (0-5), None for simple correct/incorrect
    
    Returns:
        Tuple of (new_interval, next_review_date_iso)
    """
    # If quality not provided, infer from correct
    if quality is None:
        quality = 4 if correct else 1
    
    # SM-2 Algorithm
    if quality < 3:
        # Failed - reset interval
        new_interval = 1
        new_ease = max(1.3, ease_factor - 0.2)
    else:
        # Passed
        if current_interval == 0:
            new_interval = 1
        elif current_interval == 1:
            new_interval = 6
        else:
            new_interval = int(current_interval * ease_factor)
        
        # Adjust ease factor
        new_ease = ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
        new_ease = max(1.3, min(2.5, new_ease))
    
    # Cap at maximum interval
    new_interval = min(new_interval, config.MAX_INTERVAL)
    
    # Calculate next review date
    next_review = datetime.now() + timedelta(days=new_interval)
    
    return new_interval, next_review.isoformat()


def get_review_quality(response_time_ms: int = None, hints_used: int = 0) -> int:
    """
    Calculate review quality based on various factors
    
    Quality scale (SM-2):
    5 - Perfect response
    4 - Correct response after hesitation
    3 - Correct with some difficulty
    2 - Incorrect but easily recalled correct answer
    1 - Incorrect; correct answer remembered
    0 - Complete blackout
    
    Returns quality score 0-5
    """
    base_quality = 4
    
    # Adjust based on hints used
    if hints_used > 0:
        base_quality -= hints_used
    
    # Adjust based on response time (if available)
    if response_time_ms is not None:
        if response_time_ms < 3000:  # Under 3 seconds
            base_quality = min(5, base_quality + 1)
        elif response_time_ms > 10000:  # Over 10 seconds
            base_quality = max(0, base_quality - 1)
    
    return max(0, min(5, base_quality))


def get_initial_intervals() -> dict:
    """Get initial interval settings for new words"""
    return {
        "interval": 0,
        "ease_factor": 2.5,
        "reviews": 0,
        "correct_count": 0,
    }


def estimate_review_load(
    words_status: dict,
    days_ahead: int = 7
) -> dict:
    """
    Estimate review load for upcoming days
    
    Returns dict with date -> word count mapping
    """
    now = datetime.now()
    load = {}
    
    for i in range(days_ahead):
        date = (now + timedelta(days=i)).date().isoformat()
        load[date] = 0
    
    for word_id, status in words_status.items():
        next_review = status.get("next_review")
        if next_review:
            try:
                review_date = datetime.fromisoformat(next_review).date().isoformat()
                if review_date in load:
                    load[review_date] += 1
            except ValueError:
                continue
    
    return load


def get_optimal_daily_limit(
    total_words: int,
    target_days: int,
    review_multiplier: float = 1.5
) -> int:
    """
    Calculate optimal daily new words limit based on target completion
    
    Args:
        total_words: Total words to learn
        target_days: Days to complete learning
        review_multiplier: Expected reviews per word
    
    Returns recommended daily new words
    """
    # Account for reviews taking up time
    effective_capacity = config.DAILY_NEW_WORDS + config.DAILY_REVIEW_WORDS
    review_load = effective_capacity * 0.7  # Reserve 70% for reviews eventually
    
    daily_new = min(
        total_words // target_days,
        int(effective_capacity - review_load)
    )
    
    return max(1, daily_new)


class SpacedRepetitionScheduler:
    """Manages spaced repetition scheduling for a user"""
    
    def __init__(self, user_data: dict):
        self.word_status = user_data.get("words_4000_progress", {}).get("word_status", {})
        self.custom_words = user_data.get("custom_vocabulary", [])
    
    def get_due_words(self, limit: int = None) -> list:
        """Get words due for review"""
        now = datetime.now()
        due = []
        
        # Check 4000 words status
        for word_id, status in self.word_status.items():
            if status.get("status") == "mastered":
                continue
            
            next_review = status.get("next_review")
            if next_review:
                try:
                    review_time = datetime.fromisoformat(next_review)
                    if review_time <= now:
                        due.append({
                            "word_id": word_id,
                            "is_4000": True,
                            "overdue_days": (now - review_time).days,
                            "status": status,
                        })
                except ValueError:
                    continue
        
        # Check custom words
        for word in self.custom_words:
            if word.get("status") == "mastered":
                continue
            
            next_review = word.get("next_review")
            if next_review:
                try:
                    review_time = datetime.fromisoformat(next_review)
                    if review_time <= now:
                        due.append({
                            "word_id": word.get("id"),
                            "word_data": word,
                            "is_4000": False,
                            "overdue_days": (now - review_time).days,
                            "status": word,
                        })
                except ValueError:
                    continue
        
        # Sort by overdue days (most overdue first)
        due.sort(key=lambda x: x["overdue_days"], reverse=True)
        
        if limit:
            due = due[:limit]
        
        return due
    
    def get_upcoming_reviews(self, days: int = 7) -> dict:
        """Get upcoming review schedule"""
        return estimate_review_load(self.word_status, days)
    
    def get_learning_stats(self) -> dict:
        """Get learning statistics"""
        stats = {
            "total_learned": 0,
            "new": 0,
            "learning": 0,
            "known": 0,
            "weak": 0,
            "mastered": 0,
            "due_today": 0,
        }
        
        now = datetime.now()
        today = now.date()
        
        for word_id, status in self.word_status.items():
            status_type = status.get("status", "new")
            stats[status_type] = stats.get(status_type, 0) + 1
            
            if status_type != "new":
                stats["total_learned"] += 1
            
            next_review = status.get("next_review")
            if next_review:
                try:
                    if datetime.fromisoformat(next_review).date() <= today:
                        stats["due_today"] += 1
                except ValueError:
                    pass
        
        return stats
