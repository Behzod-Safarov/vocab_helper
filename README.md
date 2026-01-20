# 📚 Vocabulary Learning Bot for Telegram

An intelligent Telegram bot designed to help students learn, remember, and test vocabulary effectively through interaction, repetition, and assessment.

## ✨ Features

### Core Features
- **📖 Learn Words** - Study vocabulary with detailed definitions, examples, and context
- **📝 Interactive Tests** - Multiple choice, fill-in-the-blank, and meaning-to-word quizzes
- **🔄 Spaced Repetition** - SM-2 algorithm for optimal review scheduling
- **📊 Progress Tracking** - Track learned words, streaks, and statistics
- **✏️ Custom Vocabulary** - Add and manage your own words

### 4000 Essential English Words
- 6 Levels (Beginner to Advanced)
- 30 Units per level
- ~20 words per unit
- Unit tests and level tests
- Progress tracking per level/unit

### Learning Modes
- **Flashcard Review** - "I Remember" / "I Forgot" buttons
- **Multiple Choice Quiz** - Word to meaning and meaning to word
- **Fill in the Blank** - Context-based learning
- **Review Mode** - Practice weak and forgotten words

## 🛠️ Setup

### Prerequisites
- Python 3.9+
- Telegram Bot Token (get from [@BotFather](https://t.me/BotFather))

### Installation

1. **Clone or download the project**

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the bot**
   
   Edit `config.py` and replace `YOUR_BOT_TOKEN_HERE` with your actual bot token:
   ```python
   BOT_TOKEN = "your_actual_bot_token"
   ```
   
   Or set an environment variable:
   ```bash
   set BOT_TOKEN=your_actual_bot_token  # Windows
   export BOT_TOKEN=your_actual_bot_token  # Linux/Mac
   ```

4. **Run the bot**
   ```bash
   python bot.py
   ```

## 📁 Project Structure

```
VOCAB_HELPER/
├── bot.py                 # Main entry point
├── config.py              # Configuration settings
├── requirements.txt       # Dependencies
├── handlers/              # Command handlers
│   ├── start.py          # /start, /help commands
│   ├── learn.py          # /learn command
│   ├── test.py           # /test command
│   ├── review.py         # /review command
│   ├── stats.py          # /stats command
│   ├── words_4000.py     # /4000words command
│   └── settings.py       # /settings command
├── modules/               # Core modules
│   ├── vocabulary.py     # Word management
│   ├── spaced_repetition.py  # SM-2 algorithm
│   ├── test_engine.py    # Quiz/test generation
│   └── progress.py       # Progress tracking
├── storage/               # Data storage
│   └── json_storage.py   # JSON file operations
├── keyboards/             # Telegram keyboards
│   └── inline.py         # Inline button keyboards
├── utils/                 # Utilities
│   └── helpers.py        # Helper functions
└── data/                  # Data files
    ├── users/            # User data (JSON)
    └── 4000_words/       # Vocabulary data
```

## 🤖 Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Start the bot and show main menu |
| `/learn` | Start a learning session |
| `/test` | Take a vocabulary test |
| `/review` | Review words due today |
| `/stats` | View your learning statistics |
| `/4000words` | Access 4000 Essential Words |
| `/settings` | Customize your experience |
| `/help` | Show help information |

## 📘 Adding More Vocabulary

### Adding 4000 Words Data

Create JSON files in `data/4000_words/` following this structure:

```json
{
  "level": 1,
  "description": "Beginner - Basic everyday words",
  "total_units": 30,
  "units": {
    "unit_1": {
      "title": "Unit 1",
      "words": [
        {
          "word": "example",
          "meaning": "a thing that is typical of a group",
          "part_of_speech": "noun",
          "example": "This is an example sentence."
        }
      ]
    }
  }
}
```

### Word Status System

Words progress through these statuses:
- **New** - Not yet studied
- **Learning** - Currently being learned
- **Known** - Correctly answered 2+ times
- **Weak** - Needs more practice
- **Mastered** - Correctly answered 5+ times in a row

## ⚙️ Configuration

Edit `config.py` to customize:

```python
# Learning Settings
DAILY_NEW_WORDS = 10        # New words per day
DAILY_REVIEW_WORDS = 20     # Review words per day
WORDS_PER_QUIZ = 10         # Questions per quiz

# Mastery Thresholds
WEAK_THRESHOLD = 2          # Correct answers to move from weak
MASTERED_THRESHOLD = 5      # Correct streak to mark as mastered

# Spaced Repetition
MAX_INTERVAL = 365          # Maximum days between reviews
```

## 🧠 Spaced Repetition Algorithm

The bot uses the SM-2 algorithm for optimal review scheduling:

1. New words start with a 1-day interval
2. Correct answers increase the interval
3. Incorrect answers decrease the interval
4. Ease factor adjusts based on performance
5. Words are scheduled for review automatically

## 📊 Data Storage

All data is stored in JSON files:
- User data: `data/users/{user_id}.json`
- Vocabulary: `data/4000_words/level_{n}.json`

No database required!

## 🤝 Contributing

Feel free to:
- Add more vocabulary data
- Improve the spaced repetition algorithm
- Add new quiz types
- Enhance the UI/UX

## 📄 License

This project is open source and available for educational purposes.

---

Made with ❤️ for vocabulary learners everywhere!
