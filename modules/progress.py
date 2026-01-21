"""
Progress Tracking Module
Handles user statistics, streaks, and progress visualization
"""
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import config


class ProgressTracker:
    """Tracks and reports user progress"""
    
    def __init__(self, user_data: Dict):
        self.user_data = user_data
        self.stats = user_data.get("stats", {})
        self.progress = user_data.get("words_4000_progress", {})
        self.custom_vocab = user_data.get("custom_vocabulary", [])
    
    def get_overall_stats(self) -> Dict:
        """Get comprehensive user statistics"""
        word_status = self.progress.get("word_status", {})
        
        # Count word statuses
        status_counts = {
            "new": 0,
            "learning": 0,
            "known": 0,
            "weak": 0,
            "mastered": 0,
        }
        
        for word_id, status in word_status.items():
            s = status.get("status", "new")
            status_counts[s] = status_counts.get(s, 0) + 1
        
        # Add custom vocabulary counts
        for word in self.custom_vocab:
            s = word.get("status", "new")
            status_counts[s] = status_counts.get(s, 0) + 1
        
        total_words = sum(status_counts.values())
        learned = status_counts["known"] + status_counts["mastered"]
        
        return {
            "total_words_started": total_words,
            "words_learning": status_counts["learning"],
            "words_known": status_counts["known"],
            "words_weak": status_counts["weak"],
            "words_mastered": status_counts["mastered"],
            "total_reviews": self.stats.get("total_reviews", 0),
            "total_tests": self.stats.get("total_tests_taken", 0),
            "correct_answers": self.stats.get("correct_answers", 0),
            "wrong_answers": self.stats.get("wrong_answers", 0),
            "accuracy": self._calculate_accuracy(),
            "current_streak": self.stats.get("current_streak", 0),
            "longest_streak": self.stats.get("longest_streak", 0),
            "last_study_date": self.stats.get("last_study_date"),
            "custom_words_count": len(self.custom_vocab),
        }
    
    def _calculate_accuracy(self) -> float:
        """Calculate overall accuracy percentage"""
        correct = self.stats.get("correct_answers", 0)
        wrong = self.stats.get("wrong_answers", 0)
        total = correct + wrong
        
        if total == 0:
            return 0.0
        
        return (correct / total) * 100
    
    def get_level_progress(self, level: int) -> Dict:
        """Get progress for a specific level"""
        word_status = self.progress.get("word_status", {})
        
        # Count words by status for this level
        level_stats = {
            "total": 0,
            "new": 0,
            "learning": 0,
            "known": 0,
            "weak": 0,
            "mastered": 0,
        }
        
        for word_id, status in word_status.items():
            if word_id.startswith(f"L{level}"):
                level_stats["total"] += 1
                s = status.get("status", "new")
                level_stats[s] = level_stats.get(s, 0) + 1
        
        # Expected total words in level
        expected_total = config.UNITS_PER_LEVEL * config.WORDS_PER_UNIT
        
        learned = level_stats["known"] + level_stats["mastered"]
        progress_pct = (learned / expected_total * 100) if expected_total > 0 else 0
        
        return {
            "level": level,
            "expected_total": expected_total,
            "started": level_stats["total"],
            "learning": level_stats["learning"],
            "known": level_stats["known"],
            "weak": level_stats["weak"],
            "mastered": level_stats["mastered"],
            "progress_percentage": progress_pct,
        }
    
    def get_unit_progress(self, level: int, unit: int) -> Dict:
        """Get progress for a specific unit"""
        word_status = self.progress.get("word_status", {})
        prefix = f"L{level}U{unit}W"
        
        unit_stats = {
            "total": config.WORDS_PER_UNIT,
            "started": 0,
            "learning": 0,
            "known": 0,
            "weak": 0,
            "mastered": 0,
        }
        
        for word_id, status in word_status.items():
            if word_id.startswith(prefix):
                unit_stats["started"] += 1
                s = status.get("status", "new")
                unit_stats[s] = unit_stats.get(s, 0) + 1
        
        learned = unit_stats["known"] + unit_stats["mastered"]
        progress_pct = (learned / unit_stats["total"] * 100) if unit_stats["total"] > 0 else 0
        
        return {
            "level": level,
            "unit": unit,
            **unit_stats,
            "progress_percentage": progress_pct,
            "is_completed": progress_pct >= 80,
        }
    
    def get_streak_info(self) -> Dict:
        """Get detailed streak information"""
        current = self.stats.get("current_streak", 0)
        longest = self.stats.get("longest_streak", 0)
        last_study = self.stats.get("last_study_date")
        
        # Check if streak is at risk
        streak_at_risk = False
        hours_until_reset = None
        
        if last_study:
            last_date = datetime.fromisoformat(last_study)
            time_since = datetime.now() - last_date
            hours_passed = time_since.total_seconds() / 3600
            
            if hours_passed > 24:
                streak_at_risk = True
                hours_until_reset = config.STREAK_RESET_HOURS - hours_passed
        
        return {
            "current_streak": current,
            "longest_streak": longest,
            "last_study_date": last_study,
            "streak_at_risk": streak_at_risk,
            "hours_until_reset": max(0, hours_until_reset) if hours_until_reset else None,
            "streak_emoji": self._get_streak_emoji(current),
        }
    
    def _get_streak_emoji(self, streak: int) -> str:
        """Get appropriate emoji for streak level"""
        if streak >= 30:
            return "🏆"
        elif streak >= 14:
            return "⚡"
        elif streak >= 7:
            return "🔥"
        elif streak >= 3:
            return "✨"
        else:
            return "📚"
    
    def get_weekly_activity(self) -> List[Dict]:
        """Get activity for the past 7 days"""
        # This would need to be tracked separately in a real implementation
        # For now, return placeholder
        today = datetime.now().date()
        activity = []
        
        for i in range(7):
            date = today - timedelta(days=6-i)
            activity.append({
                "date": date.isoformat(),
                "day_name": date.strftime("%a"),
                "reviews": 0,  # Would be tracked in real implementation
                "words_learned": 0,
            })
        
        return activity
    
    def get_weak_words_summary(self) -> Dict:
        """Get summary of weak words needing attention"""
        word_status = self.progress.get("word_status", {})
        weak_words = []
        
        for word_id, status in word_status.items():
            if status.get("status") == "weak":
                weak_words.append({
                    "word_id": word_id,
                    "reviews": status.get("reviews", 0),
                    "ease_factor": status.get("ease_factor", 2.5),
                })
        
        # Add custom weak words
        for word in self.custom_vocab:
            if word.get("status") == "weak":
                weak_words.append({
                    "word_id": word.get("id"),
                    "word": word.get("word"),
                    "is_custom": True,
                })
        
        return {
            "total_weak": len(weak_words),
            "needs_attention": len(weak_words) > 10,
            "words": weak_words[:20],  # Limit to 20
        }


def format_stats_message(stats: Dict, lang: str = "en") -> str:
    """Format statistics for display"""
    from locales import get_text
    
    lines = [
        get_text("stats_title", lang) + "\n",
        f"📚 *{get_text('stats_words_progress', lang)}:*",
        f"   • {get_text('learning', lang)}: {stats.get('words_learning', 0)}",
        f"   • {get_text('known', lang)}: {stats.get('words_known', 0)}",
        f"   • {get_text('mastered', lang)}: {stats.get('words_mastered', 0)} ⭐",
        f"   • {get_text('need_review', lang)}: {stats.get('words_weak', 0)} ⚠️",
        "",
        f"📝 *{get_text('activity', lang)}:*",
        f"   • {get_text('total_reviews', lang)}: {stats.get('total_reviews', 0)}",
        f"   • {get_text('tests_taken', lang)}: {stats.get('total_tests', 0)}",
        f"   • {get_text('accuracy', lang)}: {stats.get('accuracy', 0):.1f}%",
        "",
        f"🔥 *{get_text('streak', lang)}:*",
        f"   • {get_text('current', lang)}: {stats.get('current_streak', 0)} {get_text('days', lang)}",
        f"   • {get_text('longest', lang)}: {stats.get('longest_streak', 0)} {get_text('days', lang)}",
    ]
    
    if stats.get('custom_words_count', 0) > 0:
        lines.append(f"\n✏️ {get_text('custom_words', lang)}: {stats['custom_words_count']}")
    
    return "\n".join(lines)


def format_level_progress(progress: Dict, lang: str = "en") -> str:
    """Format level progress for display"""
    from locales import get_text
    
    pct = progress.get("progress_percentage", 0)
    bar = create_progress_bar(pct)
    
    return (
        f"📘 *{get_text('level', lang)} {progress['level']} {get_text('progress', lang)}*\n\n"
        f"{bar} {pct:.1f}%\n\n"
        f"📖 {get_text('words_started', lang)}: {progress['started']}/{progress['expected_total']}\n"
        f"📚 {get_text('learning', lang)}: {progress['learning']}\n"
        f"✅ {get_text('known', lang)}: {progress['known']}\n"
        f"⭐ {get_text('mastered', lang)}: {progress['mastered']}\n"
        f"⚠️ {get_text('need_review', lang)}: {progress['weak']}"
    )


def format_unit_progress(progress: Dict, lang: str = "en") -> str:
    """Format unit progress for display"""
    from locales import get_text
    
    pct = progress.get("progress_percentage", 0)
    bar = create_progress_bar(pct)
    status = f"✅ {get_text('completed', lang)}" if progress.get("is_completed") else f"📖 {get_text('in_progress', lang)}"
    
    return (
        f"📗 *{get_text('level', lang)} {progress['level']} • {get_text('unit', lang)} {progress['unit']}*\n\n"
        f"{bar} {pct:.1f}%\n"
        f"{get_text('status', lang)}: {status}\n\n"
        f"📚 {get_text('learning', lang)}: {progress['learning']}/{progress['total']}\n"
        f"✅ {get_text('known', lang)}: {progress['known']}\n"
        f"⭐ {get_text('mastered', lang)}: {progress['mastered']}\n"
        f"⚠️ {get_text('need_review', lang)}: {progress['weak']}"
    )


def create_progress_bar(percentage: float, length: int = 10) -> str:
    """Create a visual progress bar"""
    filled = int(percentage / 100 * length)
    empty = length - filled
    return "█" * filled + "░" * empty


def format_streak_message(streak_info: Dict, lang: str = "en") -> str:
    """Format streak information for display"""
    from locales import get_text
    
    emoji = streak_info.get("streak_emoji", "📚")
    current = streak_info.get("current_streak", 0)
    longest = streak_info.get("longest_streak", 0)
    
    lines = [
        f"{emoji} *{get_text('your_learning_streak', lang)}*\n",
        f"🔥 {get_text('current_streak', lang)}: *{current} {get_text('days', lang)}*",
        f"🏆 {get_text('longest_streak', lang)}: *{longest} {get_text('days', lang)}*",
    ]
    
    if streak_info.get("streak_at_risk"):
        hours = streak_info.get("hours_until_reset", 0)
        if hours > 0:
            lines.append(f"\n⚠️ *{get_text('streak_at_risk', lang)}*")
        else:
            lines.append(f"\n😔 {get_text('streak_reset', lang)}")
    elif current > 0:
        lines.append(f"\n✨ {get_text('keep_it_up', lang)}")
    else:
        lines.append(f"\n💪 {get_text('start_streak', lang)}")
    
    # Motivational messages based on streak
    if current >= 30:
        lines.append(f"\n🎉 {get_text('streak_30_days', lang)}")
    elif current >= 14:
        lines.append(f"\n⚡ {get_text('streak_14_days', lang)}")
    elif current >= 7:
        lines.append(f"\n🌟 {get_text('streak_7_days', lang)}")
    
    return "\n".join(lines)
