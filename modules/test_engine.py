"""
Test Engine Module
Handles quiz generation, scoring, and evaluation
"""
import random
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum


class QuestionType(Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    FILL_BLANK = "fill_blank"
    MEANING_TO_WORD = "meaning_to_word"
    WORD_TO_MEANING = "word_to_meaning"


@dataclass
class Question:
    """Represents a quiz question"""
    question_id: str
    word_id: str
    word: str
    correct_answer: str
    question_type: QuestionType
    question_text: str
    options: List[str] = field(default_factory=list)
    hint: str = None
    example: str = None
    is_4000: bool = True
    level: int = None
    unit: int = None


@dataclass
class TestResult:
    """Represents test results"""
    total_questions: int
    correct_answers: int
    wrong_answers: int
    score_percentage: float
    word_results: Dict[str, bool]  # word_id -> correct
    time_taken: int = 0  # seconds
    test_type: str = "unit"
    level: int = None
    unit: int = None
    
    @property
    def passed(self) -> bool:
        return self.score_percentage >= 70


class TestSession:
    """Manages an active test session"""
    
    def __init__(
        self,
        user_id: int,
        test_type: str,
        level: int = None,
        unit: int = None,
    ):
        self.user_id = user_id
        self.test_type = test_type
        self.level = level
        self.unit = unit
        self.questions: List[Question] = []
        self.current_index = 0
        self.answers: Dict[str, str] = {}
        self.results: Dict[str, bool] = {}
        self.started_at = datetime.now()
        self.completed = False
        self.current_streak = 0
        self.best_streak = 0
    
    def add_questions(self, questions: List[Question]):
        """Add questions to the session"""
        self.questions = questions
        random.shuffle(self.questions)
    
    def get_current_question(self) -> Optional[Question]:
        """Get the current question"""
        if self.current_index < len(self.questions):
            return self.questions[self.current_index]
        return None
    
    def answer_current(self, answer: str) -> Tuple[bool, str]:
        """
        Answer the current question
        Returns (is_correct, correct_answer)
        """
        question = self.get_current_question()
        if question is None:
            return False, ""
        
        is_correct = answer.lower().strip() == question.correct_answer.lower().strip()
        
        self.answers[question.question_id] = answer
        self.results[question.word_id] = is_correct
        
        # Update streak
        if is_correct:
            self.current_streak += 1
            if self.current_streak > self.best_streak:
                self.best_streak = self.current_streak
        else:
            self.current_streak = 0
        
        return is_correct, question.correct_answer
    
    def next_question(self) -> Optional[Question]:
        """Move to next question"""
        self.current_index += 1
        if self.current_index >= len(self.questions):
            self.completed = True
            return None
        return self.get_current_question()
    
    def get_progress(self) -> Tuple[int, int]:
        """Get current progress (answered, total)"""
        return self.current_index, len(self.questions)
    
    def get_quiz_stats(self) -> Dict:
        """Get current quiz statistics"""
        correct = sum(1 for v in self.results.values() if v)
        answered = len(self.results)
        return {
            "correct": correct,
            "wrong": answered - correct,
            "answered": answered,
            "total": len(self.questions),
            "current_streak": self.current_streak,
            "best_streak": self.best_streak,
            "percentage": (correct / answered * 100) if answered > 0 else 0,
        }
    
    def get_results(self) -> TestResult:
        """Calculate and return test results"""
        correct = sum(1 for v in self.results.values() if v)
        total = len(self.questions)
        time_taken = (datetime.now() - self.started_at).seconds
        
        return TestResult(
            total_questions=total,
            correct_answers=correct,
            wrong_answers=total - correct,
            score_percentage=(correct / total * 100) if total > 0 else 0,
            word_results=self.results.copy(),
            time_taken=time_taken,
            test_type=self.test_type,
            level=self.level,
            unit=self.unit,
        )
    
    def to_dict(self) -> Dict:
        """Convert session to dictionary for storage"""
        return {
            "user_id": self.user_id,
            "test_type": self.test_type,
            "level": self.level,
            "unit": self.unit,
            "current_index": self.current_index,
            "answers": self.answers,
            "results": self.results,
            "started_at": self.started_at.isoformat(),
            "completed": self.completed,
            "current_streak": self.current_streak,
            "best_streak": self.best_streak,
            "questions": [
                {
                    "question_id": q.question_id,
                    "word_id": q.word_id,
                    "word": q.word,
                    "correct_answer": q.correct_answer,
                    "question_type": q.question_type.value,
                    "question_text": q.question_text,
                    "options": q.options,
                    "hint": q.hint,
                    "example": q.example,
                    "is_4000": q.is_4000,
                    "level": q.level,
                    "unit": q.unit,
                }
                for q in self.questions
            ],
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "TestSession":
        """Create session from dictionary"""
        session = cls(
            user_id=data["user_id"],
            test_type=data["test_type"],
            level=data.get("level"),
            unit=data.get("unit"),
        )
        session.current_index = data["current_index"]
        session.answers = data["answers"]
        session.results = data["results"]
        session.started_at = datetime.fromisoformat(data["started_at"])
        session.completed = data["completed"]
        session.current_streak = data.get("current_streak", 0)
        session.best_streak = data.get("best_streak", 0)
        
        session.questions = [
            Question(
                question_id=q["question_id"],
                word_id=q["word_id"],
                word=q["word"],
                correct_answer=q["correct_answer"],
                question_type=QuestionType(q["question_type"]),
                question_text=q["question_text"],
                options=q["options"],
                hint=q.get("hint"),
                example=q.get("example"),
                is_4000=q.get("is_4000", True),
                level=q.get("level"),
                unit=q.get("unit"),
            )
            for q in data["questions"]
        ]
        
        return session


class QuestionGenerator:
    """Generates quiz questions from words"""
    
    def __init__(self, all_words: List[Dict] = None):
        self.all_words = all_words or []
    
    def set_word_pool(self, words: List[Dict]):
        """Set the pool of words for generating distractors"""
        self.all_words = words
    
    def generate_multiple_choice(
        self,
        word: Dict,
        question_type: QuestionType = QuestionType.WORD_TO_MEANING,
        num_options: int = 4,
    ) -> Question:
        """Generate a multiple choice question"""
        word_id = word.get("word_id", f"w_{word.get('word', '')}")
        word_text = word.get("word", "")
        meaning = word.get("meaning", "")
        example = word.get("example", "")
        
        if question_type == QuestionType.WORD_TO_MEANING:
            question_text = f"What is the meaning of *{word_text}*?"
            correct_answer = meaning
            
            # Get distractors from other words
            distractors = self._get_distractors(
                word,
                "meaning",
                num_options - 1
            )
            options = [correct_answer] + distractors
            
        else:  # MEANING_TO_WORD
            question_text = f"Which word means: _{meaning}_?"
            correct_answer = word_text
            
            distractors = self._get_distractors(
                word,
                "word",
                num_options - 1
            )
            options = [correct_answer] + distractors
        
        random.shuffle(options)
        
        return Question(
            question_id=f"q_{word_id}_{question_type.value}",
            word_id=word_id,
            word=word_text,
            correct_answer=correct_answer,
            question_type=question_type,
            question_text=question_text,
            options=options,
            example=example,
            is_4000=word.get("is_4000", True),
            level=word.get("level"),
            unit=word.get("unit"),
        )
    
    def generate_fill_blank(self, word: Dict) -> Question:
        """Generate a fill-in-the-blank question"""
        word_id = word.get("word_id", f"w_{word.get('word', '')}")
        word_text = word.get("word", "")
        meaning = word.get("meaning", "")
        example = word.get("example", "")
        
        if example and word_text.lower() in example.lower():
            # Replace word in example with blank
            import re
            pattern = re.compile(re.escape(word_text), re.IGNORECASE)
            question_text = pattern.sub("_____", example)
            question_text = f"Fill in the blank:\n\n_{question_text}_"
            hint = f"Meaning: {meaning}"
        else:
            # Use meaning as hint
            question_text = f"What word means: _{meaning}_?"
            hint = f"First letter: {word_text[0].upper()}" if word_text else None
        
        return Question(
            question_id=f"q_{word_id}_fill",
            word_id=word_id,
            word=word_text,
            correct_answer=word_text,
            question_type=QuestionType.FILL_BLANK,
            question_text=question_text,
            hint=hint,
            example=example,
            is_4000=word.get("is_4000", True),
            level=word.get("level"),
            unit=word.get("unit"),
        )
    
    def _get_distractors(
        self,
        target_word: Dict,
        field: str,
        count: int
    ) -> List[str]:
        """Get distractor options from word pool"""
        target_value = target_word.get(field, "").lower()
        distractors = []
        
        # Shuffle to randomize
        pool = self.all_words.copy()
        random.shuffle(pool)
        
        for word in pool:
            value = word.get(field, "")
            if value and value.lower() != target_value:
                distractors.append(value)
                if len(distractors) >= count:
                    break
        
        # If not enough distractors, add generic ones
        while len(distractors) < count:
            distractors.append(f"Option {len(distractors) + 1}")
        
        return distractors
    
    def generate_test(
        self,
        words: List[Dict],
        num_questions: int = 10,
        question_types: List[QuestionType] = None,
    ) -> List[Question]:
        """Generate a full test from a list of words"""
        if question_types is None:
            question_types = [
                QuestionType.WORD_TO_MEANING,
                QuestionType.MEANING_TO_WORD,
                QuestionType.FILL_BLANK,
            ]
        
        # Set word pool for distractors
        self.set_word_pool(words)
        
        questions = []
        words_sample = random.sample(words, min(num_questions, len(words)))
        
        for i, word in enumerate(words_sample):
            q_type = question_types[i % len(question_types)]
            
            if q_type == QuestionType.FILL_BLANK:
                question = self.generate_fill_blank(word)
            else:
                question = self.generate_multiple_choice(word, q_type)
            
            questions.append(question)
        
        return questions


def create_progress_bar(current: int, total: int, length: int = 10) -> str:
    """Create a visual progress bar"""
    filled = int((current / total) * length) if total > 0 else 0
    empty = length - filled
    return "🟩" * filled + "⬜" * empty


def format_question_quiz(
    question: Question, 
    progress: Tuple[int, int],
    quiz_stats: Dict = None,
    lang: str = "en"
) -> str:
    """Format a question for quiz mode display with enhanced visuals"""
    from locales import get_text
    
    lines = []
    current, total = progress
    
    # Progress bar header
    progress_bar = create_progress_bar(current, total)
    lines.append(f"📊 {progress_bar} {current + 1}/{total}")
    
    # Stats line (if available)
    if quiz_stats:
        correct = quiz_stats.get("correct", 0)
        streak = quiz_stats.get("current_streak", 0)
        stats_line = f"✅ {correct}"
        if streak >= 2:
            stats_line += f"  🔥 {streak}"
        lines.append(stats_line)
    
    lines.append("")  # Empty line
    lines.append("─" * 20)
    lines.append("")
    
    # Question text
    lines.append(question.question_text)
    
    return "\n".join(lines)


def format_question(question: Question, show_progress: Tuple[int, int] = None, lang: str = "en") -> str:
    """Format a question for display in Telegram"""
    from locales import get_text
    
    lines = []
    
    if show_progress:
        current, total = show_progress
        lines.append(get_text("test_question_progress", lang, current=current + 1, total=total) + "\n")
    
    lines.append(question.question_text)
    
    if question.options:
        lines.append("\n")
        letters = ["A", "B", "C", "D", "E", "F"]
        for i, option in enumerate(question.options):
            lines.append(f"{letters[i]}. {option}")
    
    return "\n".join(lines)


def format_result(result: TestResult, lang: str = "en", best_streak: int = 0) -> str:
    """Format test results for display"""
    from locales import get_text
    
    # Create a visual score bar
    score_filled = int(result.score_percentage / 10)
    score_bar = "🟩" * score_filled + "⬜" * (10 - score_filled)
    
    lines = [
        "🏆 " + get_text("test_results_title", lang),
        "",
        f"{score_bar}",
        f"📊 {result.score_percentage:.0f}%",
        "",
    ]
    
    if result.level and result.unit:
        lines.append(f"📚 {get_text('level', lang)} {result.level} • {get_text('unit', lang)} {result.unit}")
        lines.append("")
    
    lines.extend([
        f"✅ {get_text('correct_count', lang)}: {result.correct_answers}",
        f"❌ {get_text('wrong_count', lang)}: {result.wrong_answers}",
        f"⏱ {get_text('time', lang)}: {result.time_taken // 60}{get_text('min', lang)} {result.time_taken % 60}{get_text('sec', lang)}",
    ])
    
    if best_streak >= 2:
        lines.append(f"🔥 {get_text('best_streak', lang)}: {best_streak}")
    
    lines.append("")
    
    # Add emoji based on score
    if result.score_percentage >= 90:
        lines.append("🌟 " + get_text("result_excellent", lang))
    elif result.score_percentage >= 70:
        lines.append("👏 " + get_text("result_great", lang))
    elif result.score_percentage >= 50:
        lines.append("💪 " + get_text("result_good", lang))
    else:
        lines.append("📚 " + get_text("result_keep_trying", lang))
    
    return "\n".join(lines)


def evaluate_answer(user_answer: str, correct_answer: str, strict: bool = False) -> bool:
    """
    Evaluate if user's answer is correct
    
    Args:
        user_answer: User's provided answer
        correct_answer: The correct answer
        strict: If True, requires exact match; if False, allows minor variations
    """
    user_clean = user_answer.lower().strip()
    correct_clean = correct_answer.lower().strip()
    
    if strict:
        return user_clean == correct_clean
    
    # Allow minor typos for fill-in-blank (Levenshtein distance of 1)
    if len(user_clean) >= 4:
        # Simple check: same first 3 chars and similar length
        if (user_clean[:3] == correct_clean[:3] and 
            abs(len(user_clean) - len(correct_clean)) <= 1):
            return True
    
    return user_clean == correct_clean
