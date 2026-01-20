"""
Configuration settings for the Vocabulary Learning Bot
"""
import os

# Bot Token - Get from @BotFather on Telegram
# BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
BOT_TOKEN = "7839287725:AAFMLZCqS8Db8DUNAYrTcfOHALO8pHQYBQs"

# Data directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
USERS_DIR = os.path.join(DATA_DIR, "users")
WORDS_4000_DIR = os.path.join(DATA_DIR, "4000_words")

# Spaced Repetition Settings
INITIAL_INTERVAL = 1  # Days before first review
EASY_BONUS = 1.3
INTERVAL_MODIFIER = 1.0
MAX_INTERVAL = 365  # Maximum days between reviews

# Learning Settings
DAILY_NEW_WORDS = 10
DAILY_REVIEW_WORDS = 20
WORDS_PER_QUIZ = 10

# 4000 Words Structure
LEVELS = 6
UNITS_PER_LEVEL = 30
WORDS_PER_UNIT = 20

# Mastery Thresholds
WEAK_THRESHOLD = 2  # Correct answers needed to move from weak
MASTERED_THRESHOLD = 5  # Correct streak to mark as mastered

# Streak Settings
STREAK_RESET_HOURS = 48  # Hours of inactivity before streak resets

# Messages
WELCOME_MESSAGE = """
🎓 *Welcome to Vocabulary Coach!*

I'm your personal vocabulary learning assistant. I'll help you:

📚 Learn new words with spaced repetition
🧠 Test your knowledge with interactive quizzes  
📊 Track your progress and build streaks

*Quick Commands:*
/learn - Start learning session
/test - Take a vocabulary test
/review - Review words due today
/stats - View your progress
/4000words - Access 4000 Essential Words
/settings - Customize your experience

Let's build your vocabulary together! 💪
"""

MOTIVATION_MESSAGES = [
    "Great job! Keep up the momentum! 🚀",
    "You're making excellent progress! ⭐",
    "Every word learned is a step forward! 📈",
    "Consistency is key - you're doing amazing! 💪",
    "Your vocabulary is growing stronger! 🌱",
]

ENCOURAGEMENT_MESSAGES = [
    "No worries — forgetting is part of learning 💪",
    "Don't give up! Every mistake is a learning opportunity 📚",
    "You'll get it next time! Keep practicing ✨",
    "Learning takes time. You're doing great! 🌟",
    "Stay positive! Progress isn't always linear 📈",
]
