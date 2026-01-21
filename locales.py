"""
Localization module for multi-language support
Supports: English (en), Uzbek (uz), Russian (ru)
"""
from typing import Dict

# Available languages
LANGUAGES = {
    "en": "🇬🇧 English",
    "uz": "🇺🇿 O'zbekcha",
    "ru": "🇷🇺 Русский",
}

DEFAULT_LANGUAGE = "en"

# All translations
TEXTS: Dict[str, Dict[str, str]] = {
    # ============ Welcome & Start ============
    "welcome_message": {
        "en": """
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
""",
        "uz": """
🎓 *Vocabulary Coach-ga xush kelibsiz!*

Men sizning shaxsiy lug'at o'rganish yordamchingizman. Men sizga yordam beraman:

📚 Intervallik takrorlash bilan yangi so'zlarni o'rganish
🧠 Interaktiv viktorinalar bilan bilimingizni sinash
📊 Taraqqiyotingizni kuzatish

*Tezkor buyruqlar:*
/learn - O'rganishni boshlash
/test - Lug'at testini topshirish
/review - Bugungi so'zlarni takrorlash
/stats - Taraqqiyotni ko'rish
/4000words - 4000 ta muhim so'zlar
/settings - Sozlamalar

Keling, lug'atingizni birga boyitamiz! 💪
""",
        "ru": """
🎓 *Добро пожаловать в Vocabulary Coach!*

Я ваш персональный помощник по изучению слов. Я помогу вам:

📚 Учить новые слова с интервальным повторением
🧠 Проверять знания с помощью тестов
📊 Отслеживать прогресс

*Быстрые команды:*
/learn - Начать обучение
/test - Пройти тест
/review - Повторить слова на сегодня
/stats - Посмотреть прогресс
/4000words - 4000 важных слов
/settings - Настройки

Давайте расширять словарный запас вместе! 💪
""",
    },
    
    # ============ Main Menu ============
    "main_menu_title": {
        "en": "📚 *Vocabulary Coach*\n\nWhat would you like to do?",
        "uz": "📚 *Vocabulary Coach*\n\nNima qilmoqchisiz?",
        "ru": "📚 *Vocabulary Coach*\n\nЧто вы хотите сделать?",
    },
    "btn_learn": {
        "en": "📚 Learn",
        "uz": "📚 O'rganish",
        "ru": "📚 Учить",
    },
    "btn_test": {
        "en": "📝 Test",
        "uz": "📝 Test",
        "ru": "📝 Тест",
    },
    "btn_review": {
        "en": "🔄 Review",
        "uz": "🔄 Takrorlash",
        "ru": "🔄 Повторить",
    },
    "btn_stats": {
        "en": "📊 Stats",
        "uz": "📊 Statistika",
        "ru": "📊 Статистика",
    },
    "btn_4000words": {
        "en": "📘 4000 Words",
        "uz": "📘 4000 so'z",
        "ru": "📘 4000 слов",
    },
    "btn_settings": {
        "en": "⚙️ Settings",
        "uz": "⚙️ Sozlamalar",
        "ru": "⚙️ Настройки",
    },
    "btn_back": {
        "en": "◀️ Back",
        "uz": "◀️ Orqaga",
        "ru": "◀️ Назад",
    },
    "btn_main_menu": {
        "en": "◀️ Main Menu",
        "uz": "◀️ Bosh menyu",
        "ru": "◀️ Главное меню",
    },
    
    # ============ Learn Section ============
    "learn_menu_title": {
        "en": "📚 *Learning Mode*\n\nChoose what you'd like to learn:",
        "uz": "📚 *O'rganish rejimi*\n\nNimani o'rganmoqchisiz:",
        "ru": "📚 *Режим обучения*\n\nЧто вы хотите изучать:",
    },
    "btn_4000_essential": {
        "en": "📘 4000 Essential Words",
        "uz": "📘 4000 muhim so'z",
        "ru": "📘 4000 важных слов",
    },
    "btn_my_custom_words": {
        "en": "✏️ My Custom Words",
        "uz": "✏️ Mening so'zlarim",
        "ru": "✏️ Мои слова",
    },
    "btn_review_due": {
        "en": "🔄 Review Due Words",
        "uz": "🔄 Takrorlanishi kerak so'zlar",
        "ru": "🔄 Слова на повторение",
    },
    "btn_add_word": {
        "en": "➕ Add New Word",
        "uz": "➕ Yangi so'z qo'shish",
        "ru": "➕ Добавить слово",
    },
    "select_level": {
        "en": "📘 *4000 Essential English Words*\n\nSelect a level to learn:",
        "uz": "📘 *4000 muhim inglizcha so'zlar*\n\nDarajani tanlang:",
        "ru": "📘 *4000 важных английских слов*\n\nВыберите уровень:",
    },
    "level_progress": {
        "en": "📘 *Level {level}*\n\n📊 Progress: {rate:.1f}%\n✅ Learned: {learned}/{total}\n\nSelect a unit:",
        "uz": "📘 *{level}-daraja*\n\n📊 Progress: {rate:.1f}%\n✅ O'rganilgan: {learned}/{total}\n\nBo'limni tanlang:",
        "ru": "📘 *Уровень {level}*\n\n📊 Прогресс: {rate:.1f}%\n✅ Изучено: {learned}/{total}\n\nВыберите раздел:",
    },
    "btn_back_to_levels": {
        "en": "◀️ Back to Levels",
        "uz": "◀️ Darajalarga qaytish",
        "ru": "◀️ К уровням",
    },
    
    # ============ Word Learning ============
    "word_counter": {
        "en": "📖 *Level {level} • Unit {unit}* (Word {current}/{total})",
        "uz": "📖 *{level}-daraja • {unit}-bo'lim* (So'z {current}/{total})",
        "ru": "📖 *Уровень {level} • Раздел {unit}* (Слово {current}/{total})",
    },
    "meaning_label": {
        "en": "📖 *Meaning:*",
        "uz": "📖 *Ma'nosi:*",
        "ru": "📖 *Значение:*",
    },
    "meaning_uz_label": {
        "en": "🇺🇿 *Uzbek:*",
        "uz": "🇺🇿 *O'zbekcha:*",
        "ru": "🇺🇿 *Узбекский:*",
    },
    "meaning_ru_label": {
        "en": "🇷🇺 *Russian:*",
        "uz": "🇷🇺 *Ruscha:*",
        "ru": "🇷🇺 *Русский:*",
    },
    "example_label": {
        "en": "💬 *Example:*",
        "uz": "💬 *Misol:*",
        "ru": "💬 *Пример:*",
    },
    "synonyms_label": {
        "en": "🔄 *Synonyms:*",
        "uz": "🔄 *Sinonimlar:*",
        "ru": "🔄 *Синонимы:*",
    },
    "btn_i_know": {
        "en": "✅ I Know This",
        "uz": "✅ Bilaman",
        "ru": "✅ Знаю",
    },
    "btn_i_dont_know": {
        "en": "❌ I Don't Know",
        "uz": "❌ Bilmayman",
        "ru": "❌ Не знаю",
    },
    "btn_pronunciation": {
        "en": "🔊 Pronunciation",
        "uz": "🔊 Talaffuz",
        "ru": "🔊 Произношение",
    },
    "pronunciation_not_available": {
        "en": "Pronunciation not available for this word",
        "uz": "Bu so'z uchun talaffuz mavjud emas",
        "ru": "Произношение недоступно для этого слова",
    },
    "pronunciation_error": {
        "en": "Error playing pronunciation. Please try again.",
        "uz": "Talaffuzni ijro etishda xatolik. Qaytadan urinib ko'ring.",
        "ru": "Ошибка воспроизведения. Попробуйте снова.",
    },
    "tts_not_installed": {
        "en": "Text-to-speech is not available. Please install gTTS.",
        "uz": "Matnni nutqqa aylantirish mavjud emas. gTTS o'rnating.",
        "ru": "Преобразование текста в речь недоступно. Установите gTTS.",
    },
    "btn_example": {
        "en": "📝 Example",
        "uz": "📝 Misol",
        "ru": "📝 Пример",
    },
    "btn_next_word": {
        "en": "⏭ Next Word",
        "uz": "⏭ Keyingi so'z",
        "ru": "⏭ Следующее слово",
    },
    "btn_show_answer": {
        "en": "👁 Show Answer",
        "uz": "👁 Javobni ko'rsatish",
        "ru": "👁 Показать ответ",
    },
    "btn_end_session": {
        "en": "◀️ End Session",
        "uz": "◀️ Yakunlash",
        "ru": "◀️ Завершить",
    },
    "btn_i_remember": {
        "en": "✅ I Remember",
        "uz": "✅ Esladim",
        "ru": "✅ Помню",
    },
    "btn_i_forgot": {
        "en": "❌ I Forgot",
        "uz": "❌ Unutdim",
        "ru": "❌ Забыл",
    },
    
    # ============ Test Section ============
    "test_menu_title": {
        "en": "📝 *Test Mode*\n\nTest your vocabulary knowledge!",
        "uz": "📝 *Test rejimi*\n\nLug'at bilimingizni sinab ko'ring!",
        "ru": "📝 *Режим теста*\n\nПроверьте свои знания!",
    },
    "btn_quick_test": {
        "en": "⚡ Quick Test (10 words)",
        "uz": "⚡ Tezkor test (10 so'z)",
        "ru": "⚡ Быстрый тест (10 слов)",
    },
    "btn_full_test": {
        "en": "📋 Full Test (20 words)",
        "uz": "📋 To'liq test (20 so'z)",
        "ru": "📋 Полный тест (20 слов)",
    },
    "btn_level_test": {
        "en": "📘 Test by Level",
        "uz": "📘 Daraja bo'yicha test",
        "ru": "📘 Тест по уровню",
    },
    "test_question": {
        "en": "❓ *Question {current}/{total}*\n\nWhat is the meaning of:\n\n📚 *{word}*",
        "uz": "❓ *Savol {current}/{total}*\n\nQuyidagi so'zning ma'nosi nima:\n\n📚 *{word}*",
        "ru": "❓ *Вопрос {current}/{total}*\n\nЧто означает:\n\n📚 *{word}*",
    },
    "test_correct": {
        "en": "✅ *Correct!*\n\n",
        "uz": "✅ *To'g'ri!*\n\n",
        "ru": "✅ *Правильно!*\n\n",
    },
    "test_wrong": {
        "en": "❌ *Wrong!*\n\nThe correct answer was:\n",
        "uz": "❌ *Noto'g'ri!*\n\nTo'g'ri javob:\n",
        "ru": "❌ *Неправильно!*\n\nПравильный ответ:\n",
    },
    "test_complete": {
        "en": "🎉 *Test Complete!*\n\n📊 Score: {correct}/{total} ({percent}%)\n\n",
        "uz": "🎉 *Test yakunlandi!*\n\n📊 Natija: {correct}/{total} ({percent}%)\n\n",
        "ru": "🎉 *Тест завершён!*\n\n📊 Результат: {correct}/{total} ({percent}%)\n\n",
    },
    "btn_next_question": {
        "en": "➡️ Next",
        "uz": "➡️ Keyingi",
        "ru": "➡️ Далее",
    },
    "btn_prev_page": {
        "en": "◀️ Prev",
        "uz": "◀️ Oldingi",
        "ru": "◀️ Назад",
    },
    "btn_next_page": {
        "en": "Next ▶️",
        "uz": "Keyingi ▶️",
        "ru": "Далее ▶️",
    },
    "btn_unit_test": {
        "en": "📝 Unit Test",
        "uz": "📝 Bo'lim testi",
        "ru": "📝 Тест раздела",
    },
    "btn_level_test_menu": {
        "en": "📚 Level Test",
        "uz": "📚 Daraja testi",
        "ru": "📚 Тест уровня",
    },
    "btn_review_test": {
        "en": "🔄 Review Test",
        "uz": "🔄 Takrorlash testi",
        "ru": "🔄 Тест повторения",
    },
    "btn_custom_test": {
        "en": "✏️ Custom Words Test",
        "uz": "✏️ Shaxsiy so'zlar testi",
        "ru": "✏️ Тест своих слов",
    },
    "btn_hint": {
        "en": "💡 Hint",
        "uz": "💡 Yordam",
        "ru": "💡 Подсказка",
    },
    "btn_skip": {
        "en": "⏭ Skip",
        "uz": "⏭ O'tkazib yuborish",
        "ru": "⏭ Пропустить",
    },
    "btn_end_test": {
        "en": "🏁 End Test",
        "uz": "🏁 Testni tugatish",
        "ru": "🏁 Завершить тест",
    },
    "btn_retry_test": {
        "en": "🔄 Retry Test",
        "uz": "🔄 Qayta urinish",
        "ru": "🔄 Повторить тест",
    },
    "btn_view_details": {
        "en": "📊 View Details",
        "uz": "📊 Batafsil ko'rish",
        "ru": "📊 Подробности",
    },
    "btn_new_test": {
        "en": "📝 New Test",
        "uz": "📝 Yangi test",
        "ru": "📝 Новый тест",
    },
    "btn_schedule": {
        "en": "📅 Schedule",
        "uz": "📅 Jadval",
        "ru": "📅 Расписание",
    },
    "btn_overall_stats": {
        "en": "📊 Overall Stats",
        "uz": "📊 Umumiy statistika",
        "ru": "📊 Общая статистика",
    },
    "btn_level_progress": {
        "en": "📘 Level Progress",
        "uz": "📘 Daraja bo'yicha",
        "ru": "📘 Прогресс уровней",
    },
    "btn_streak_info": {
        "en": "🔥 Streak Info",
        "uz": "🔥 Streak ma'lumoti",
        "ru": "🔥 Серия дней",
    },
    "btn_weak_words_stats": {
        "en": "⚠️ Weak Words",
        "uz": "⚠️ Qiyin so'zlar",
        "ru": "⚠️ Сложные слова",
    },
    "btn_confirm": {
        "en": "✅ Confirm",
        "uz": "✅ Tasdiqlash",
        "ru": "✅ Подтвердить",
    },
    "btn_cancel": {
        "en": "❌ Cancel",
        "uz": "❌ Bekor qilish",
        "ru": "❌ Отмена",
    },
    
    # ============ Review Section ============
    "review_menu_title": {
        "en": "🔄 *Review Mode*\n\nPractice words you've learned:",
        "uz": "🔄 *Takrorlash rejimi*\n\nO'rgangan so'zlaringizni mashq qiling:",
        "ru": "🔄 *Режим повторения*\n\nПрактикуйте изученные слова:",
    },
    "btn_review_due_words": {
        "en": "📅 Review Due Words",
        "uz": "📅 Bugungi so'zlar",
        "ru": "📅 Слова на сегодня",
    },
    "btn_review_weak": {
        "en": "💪 Practice Weak Words",
        "uz": "💪 Qiyin so'zlarni mashq qilish",
        "ru": "💪 Сложные слова",
    },
    "btn_review_all": {
        "en": "📚 Review All Words",
        "uz": "📚 Barcha so'zlarni takrorlash",
        "ru": "📚 Повторить все слова",
    },
    "btn_start_review": {
        "en": "🔄 Start Review",
        "uz": "🔄 Takrorlashni boshlash",
        "ru": "🔄 Начать повторение",
    },
    "btn_start_review_due": {
        "en": "🔄 Start Review ({count} due)",
        "uz": "🔄 Takrorlashni boshlash ({count} ta)",
        "ru": "🔄 Начать повторение ({count} слов)",
    },
    "no_words_to_review": {
        "en": "🎉 *Great job!*\n\nNo words to review right now. Come back later or learn new words!",
        "uz": "🎉 *Ajoyib!*\n\nHozircha takrorlanadigan so'z yo'q. Keyinroq qayting yoki yangi so'zlar o'rganing!",
        "ru": "🎉 *Отлично!*\n\nСейчас нет слов для повторения. Вернитесь позже или учите новые слова!",
    },
    "words_due_today": {
        "en": "📅 *Words Due Today: {count}*\n\nLet's review them!",
        "uz": "📅 *Bugungi so'zlar: {count}*\n\nKeling, takrorlaymiz!",
        "ru": "📅 *Слов на сегодня: {count}*\n\nДавайте повторим!",
    },
    
    # ============ Stats Section ============
    "stats_title": {
        "en": "📊 *Your Statistics*",
        "uz": "📊 *Sizning statistikangiz*",
        "ru": "📊 *Ваша статистика*",
    },
    "stats_words_learned": {
        "en": "📚 Words Learned:",
        "uz": "📚 O'rganilgan so'zlar:",
        "ru": "📚 Изучено слов:",
    },
    "stats_total_reviews": {
        "en": "🔄 Total Reviews:",
        "uz": "🔄 Jami takrorlashlar:",
        "ru": "🔄 Всего повторений:",
    },
    "stats_tests_taken": {
        "en": "📝 Tests Taken:",
        "uz": "📝 Topshirilgan testlar:",
        "ru": "📝 Пройдено тестов:",
    },
    "stats_accuracy": {
        "en": "🎯 Accuracy:",
        "uz": "🎯 Aniqlik:",
        "ru": "🎯 Точность:",
    },
    "stats_current_streak": {
        "en": "🔥 Current Streak:",
        "uz": "🔥 Joriy seriya:",
        "ru": "🔥 Текущая серия:",
    },
    "stats_longest_streak": {
        "en": "🏆 Longest Streak:",
        "uz": "🏆 Eng uzun seriya:",
        "ru": "🏆 Лучшая серия:",
    },
    "stats_days": {
        "en": "days",
        "uz": "kun",
        "ru": "дн.",
    },
    
    # ============ Settings Section ============
    "settings_title": {
        "en": "⚙️ *Settings*\n\nCustomize your learning experience:",
        "uz": "⚙️ *Sozlamalar*\n\nO'rganish tajribangizni sozlang:",
        "ru": "⚙️ *Настройки*\n\nНастройте ваше обучение:",
    },
    "btn_language": {
        "en": "🌐 Language",
        "uz": "🌐 Til",
        "ru": "🌐 Язык",
    },
    "btn_translation_lang": {
        "en": "🔤 Translation Language",
        "uz": "🔤 Tarjima tili",
        "ru": "🔤 Язык перевода",
    },
    "btn_daily_words": {
        "en": "📚 Daily New Words",
        "uz": "📚 Kunlik yangi so'zlar",
        "ru": "📚 Новых слов в день",
    },
    "btn_review_words": {
        "en": "🔄 Daily Review Words",
        "uz": "🔄 Kunlik takrorlash",
        "ru": "🔄 Повторений в день",
    },
    "btn_notifications": {
        "en": "🔔 Notifications",
        "uz": "🔔 Bildirishnomalar",
        "ru": "🔔 Уведомления",
    },
    "btn_reminder_time": {
        "en": "⏰ Reminder Time",
        "uz": "⏰ Eslatma vaqti",
        "ru": "⏰ Время напоминания",
    },
    "notifications_on": {
        "en": "ON",
        "uz": "Yoqilgan",
        "ru": "ВКЛ",
    },
    "notifications_off": {
        "en": "OFF",
        "uz": "O'chirilgan",
        "ru": "ВЫКЛ",
    },
    "select_language": {
        "en": "🌐 *Select Interface Language*\n\nChoose your preferred language:",
        "uz": "🌐 *Interfeys tilini tanlang*\n\nO'zingizga qulay tilni tanlang:",
        "ru": "🌐 *Выберите язык интерфейса*\n\nВыберите предпочтительный язык:",
    },
    "select_translation": {
        "en": "🔤 *Select Translation Language*\n\nChoose which translation to show with words:",
        "uz": "🔤 *Tarjima tilini tanlang*\n\nSo'zlar bilan qaysi tarjimani ko'rsatishni tanlang:",
        "ru": "🔤 *Выберите язык перевода*\n\nВыберите, какой перевод показывать:",
    },
    "translation_both": {
        "en": "🌍 Both (Uzbek + Russian)",
        "uz": "🌍 Ikkala (O'zbekcha + Ruscha)",
        "ru": "🌍 Оба (Узбекский + Русский)",
    },
    "translation_uz": {
        "en": "🇺🇿 Uzbek Only",
        "uz": "🇺🇿 Faqat o'zbekcha",
        "ru": "🇺🇿 Только узбекский",
    },
    "translation_ru": {
        "en": "🇷🇺 Russian Only",
        "uz": "🇷🇺 Faqat ruscha",
        "ru": "🇷🇺 Только русский",
    },
    "translation_none": {
        "en": "🇬🇧 English Only (No Translation)",
        "uz": "🇬🇧 Faqat inglizcha (Tarjimasiz)",
        "ru": "🇬🇧 Только английский (Без перевода)",
    },
    "language_changed": {
        "en": "✅ Language changed to English",
        "uz": "✅ Til o'zbekchaga o'zgartirildi",
        "ru": "✅ Язык изменён на русский",
    },
    "translation_changed": {
        "en": "✅ Translation language updated",
        "uz": "✅ Tarjima tili yangilandi",
        "ru": "✅ Язык перевода обновлён",
    },
    "daily_words_title": {
        "en": "📚 *Daily New Words*\n\nHow many new words do you want to learn per day?",
        "uz": "📚 *Kunlik yangi so'zlar*\n\nKuniga nechta yangi so'z o'rganmoqchisiz?",
        "ru": "📚 *Новых слов в день*\n\nСколько новых слов вы хотите учить в день?",
    },
    "daily_review_title": {
        "en": "🔄 *Daily Review Words*\n\nHow many words do you want to review per day?",
        "uz": "🔄 *Kunlik takrorlash*\n\nKuniga nechta so'z takrorlamoqchisiz?",
        "ru": "🔄 *Повторений в день*\n\nСколько слов вы хотите повторять в день?",
    },
    "reminder_time_title": {
        "en": "⏰ *Reminder Time*\n\nSelect when you'd like to receive daily reminders:",
        "uz": "⏰ *Eslatma vaqti*\n\nKunlik eslatmalarni qachon olishni xohlaysiz:",
        "ru": "⏰ *Время напоминания*\n\nВыберите время для ежедневных напоминаний:",
    },
    
    # ============ Help Section ============
    "help_title": {
        "en": "📖 *Vocabulary Coach Help*",
        "uz": "📖 *Vocabulary Coach Yordam*",
        "ru": "📖 *Справка Vocabulary Coach*",
    },
    "help_commands": {
        "en": """
*Commands:*
/start - Start the bot
/learn - Start a learning session
/test - Take a vocabulary test
/review - Review words due today
/stats - View your progress
/4000words - Access 4000 Essential Words
/settings - Customize your experience

*How it works:*
1️⃣ Learn new words from 4000 Essential Words or add your own
2️⃣ Practice with flashcards and quizzes
3️⃣ Review words using spaced repetition
4️⃣ Track your progress and build streaks

*Tips:*
• Study a little every day for best results
• Don't skip reviews - they help you remember!
• Use the "I forgot" button honestly
• Try to complete one unit before moving on

Need more help? Just start exploring! 📚
""",
        "uz": """
*Buyruqlar:*
/start - Botni ishga tushirish
/learn - O'rganishni boshlash
/test - Lug'at testini topshirish
/review - Bugungi so'zlarni takrorlash
/stats - Taraqqiyotni ko'rish
/4000words - 4000 muhim so'zlar
/settings - Sozlamalar

*Qanday ishlaydi:*
1️⃣ 4000 muhim so'zlardan yangi so'zlar o'rganing yoki o'zingiznikini qo'shing
2️⃣ Kartochkalar va viktorinalar bilan mashq qiling
3️⃣ Intervallik takrorlash yordamida so'zlarni takrorlang
4️⃣ Taraqqiyotingizni kuzating

*Maslahatlar:*
• Eng yaxshi natijalar uchun har kuni biroz o'rganing
• Takrorlashlarni o'tkazib yubormang!
• "Unutdim" tugmasini halol ishlating
• Keyingisiga o'tishdan oldin bitta bo'limni yakunlang

Ko'proq yordam kerakmi? Shunchaki o'rganishni boshlang! 📚
""",
        "ru": """
*Команды:*
/start - Запустить бота
/learn - Начать обучение
/test - Пройти тест
/review - Повторить слова на сегодня
/stats - Посмотреть прогресс
/4000words - 4000 важных слов
/settings - Настройки

*Как это работает:*
1️⃣ Учите новые слова из 4000 важных слов или добавляйте свои
2️⃣ Практикуйтесь с карточками и тестами
3️⃣ Повторяйте слова с интервальным повторением
4️⃣ Отслеживайте прогресс

*Советы:*
• Учите понемногу каждый день
• Не пропускайте повторения!
• Используйте кнопку "Забыл" честно
• Завершите один раздел перед переходом к следующему

Нужна помощь? Просто начните изучать! 📚
""",
    },
    
    # ============ Motivation Messages ============
    "motivation_1": {
        "en": "Great job! Keep up the momentum! 🚀",
        "uz": "Ajoyib! Shu zaylda davom eting! 🚀",
        "ru": "Отлично! Продолжайте в том же духе! 🚀",
    },
    "motivation_2": {
        "en": "You're making excellent progress! ⭐",
        "uz": "Siz ajoyib taraqqiyot qilyapsiz! ⭐",
        "ru": "Вы делаете отличные успехи! ⭐",
    },
    "motivation_3": {
        "en": "Every word learned is a step forward! 📈",
        "uz": "Har bir o'rganilgan so'z oldinga qadam! 📈",
        "ru": "Каждое выученное слово - шаг вперёд! 📈",
    },
    "motivation_4": {
        "en": "Consistency is key - you're doing amazing! 💪",
        "uz": "Izchillik kalit - siz ajoyib qilyapsiz! 💪",
        "ru": "Постоянство - ключ к успеху! 💪",
    },
    "motivation_5": {
        "en": "Your vocabulary is growing stronger! 🌱",
        "uz": "Lug'atingiz kuchaymoqda! 🌱",
        "ru": "Ваш словарный запас растёт! 🌱",
    },
    
    # ============ Encouragement Messages ============
    "encouragement_1": {
        "en": "No worries — forgetting is part of learning 💪",
        "uz": "Xavotir olmang — unutish o'rganishning bir qismi 💪",
        "ru": "Не переживайте — забывать это нормально 💪",
    },
    "encouragement_2": {
        "en": "Don't give up! Every mistake is a learning opportunity 📚",
        "uz": "Taslim bo'lmang! Har bir xato — o'rganish imkoniyati 📚",
        "ru": "Не сдавайтесь! Каждая ошибка — возможность учиться 📚",
    },
    "encouragement_3": {
        "en": "You'll get it next time! Keep practicing ✨",
        "uz": "Keyingi safar albatta eslab qolasiz! Mashq qilishda davom eting ✨",
        "ru": "В следующий раз получится! Продолжайте практиковаться ✨",
    },
    "encouragement_4": {
        "en": "Learning takes time. You're doing great! 🌟",
        "uz": "O'rganish vaqt talab qiladi. Siz ajoyib qilyapsiz! 🌟",
        "ru": "Обучение требует времени. У вас отлично получается! 🌟",
    },
    "encouragement_5": {
        "en": "Stay positive! Progress isn't always linear 📈",
        "uz": "Ijobiy bo'ling! Taraqqiyot har doim ham to'g'ri chiziqda bo'lmaydi 📈",
        "ru": "Будьте позитивны! Прогресс не всегда линеен 📈",
    },
    
    # ============ Unit/Level Completion ============
    "unit_complete": {
        "en": "🎉 *Congratulations!*\n\nYou've completed Unit {unit} of Level {level}!",
        "uz": "🎉 *Tabriklaymiz!*\n\nSiz {level}-darajaning {unit}-bo'limini yakunladingiz!",
        "ru": "🎉 *Поздравляем!*\n\nВы завершили Раздел {unit} Уровня {level}!",
    },
    "level_complete": {
        "en": "🏆 *Amazing!*\n\nYou've completed Level {level}!",
        "uz": "🏆 *Ajoyib!*\n\nSiz {level}-darajani yakunladingiz!",
        "ru": "🏆 *Потрясающе!*\n\nВы завершили Уровень {level}!",
    },
    "word_progress": {
        "en": "📖 *Level {level} • Unit {unit}* (Word {current}/{total})",
        "uz": "📖 *{level}-daraja • {unit}-bo'lim* (So'z {current}/{total})",
        "ru": "📖 *Уровень {level} • Раздел {unit}* (Слово {current}/{total})",
    },
    
    # ============ Custom Words ============
    "custom_words_empty": {
        "en": "✏️ *My Custom Words*\n\nYou haven't added any custom words yet.\n\nTap 'Add New Word' to start building your vocabulary!",
        "uz": "✏️ *Mening so'zlarim*\n\nSiz hali maxsus so'zlar qo'shmagansiz.\n\n'Yangi so'z qo'shish' tugmasini bosing!",
        "ru": "✏️ *Мои слова*\n\nВы ещё не добавили слов.\n\nНажмите 'Добавить слово', чтобы начать!",
    },
    "custom_words_list": {
        "en": "✏️ *My Custom Words* ({count} words)\n\n{word_list}\n{more}",
        "uz": "✏️ *Mening so'zlarim* ({count} so'z)\n\n{word_list}\n{more}",
        "ru": "✏️ *Мои слова* ({count} слов)\n\n{word_list}\n{more}",
    },
    "add_word_prompt": {
        "en": "➕ *Add New Word*\n\nPlease send me the word you want to add:",
        "uz": "➕ *Yangi so'z qo'shish*\n\nIltimos, qo'shmoqchi bo'lgan so'zingizni yuboring:",
        "ru": "➕ *Добавить слово*\n\nПожалуйста, отправьте слово, которое хотите добавить:",
    },
    "add_word_meaning_prompt": {
        "en": "✅ Word: *{word}*\n\nNow send me the meaning/definition:",
        "uz": "✅ So'z: *{word}*\n\nEndi ma'nosini yuboring:",
        "ru": "✅ Слово: *{word}*\n\nТеперь отправьте значение/определение:",
    },
    "add_word_example_prompt": {
        "en": "📝 Great! Now send an example sentence.\n\n(Or send /skip to skip this step)",
        "uz": "📝 Ajoyib! Endi misol jumlani yuboring.\n\n(Yoki /skip buyrug'ini yuboring)",
        "ru": "📝 Отлично! Теперь отправьте пример предложения.\n\n(Или отправьте /skip чтобы пропустить)",
    },
    "word_added_success": {
        "en": "✅ *Word Added Successfully!*\n\n📚 Word: *{word}*\n📖 Meaning: {meaning}\n💬 Example: {example}",
        "uz": "✅ *So'z muvaffaqiyatli qo'shildi!*\n\n📚 So'z: *{word}*\n📖 Ma'nosi: {meaning}\n💬 Misol: {example}",
        "ru": "✅ *Слово успешно добавлено!*\n\n📚 Слово: *{word}*\n📖 Значение: {meaning}\n💬 Пример: {example}",
    },
    "not_provided": {
        "en": "Not provided",
        "uz": "Berilmagan",
        "ru": "Не указано",
    },
    "try_again": {
        "en": "Please try again:",
        "uz": "Iltimos, qaytadan urinib ko'ring:",
        "ru": "Пожалуйста, попробуйте ещё раз:",
    },
    
    # ============ Review Section Extended ============
    "review_all_caught_up": {
        "en": "✨ *All caught up!*\n\nYou don't have any words due for review right now.\nKeep learning new words or check back later!",
        "uz": "✨ *Hammasi bajarildi!*\n\nHozircha takrorlanadigan so'zlar yo'q.\nYangi so'zlar o'rganing yoki keyinroq qayting!",
        "ru": "✨ *Всё повторено!*\n\nСейчас нет слов для повторения.\nУчите новые слова или вернитесь позже!",
    },
    "review_progress": {
        "en": "🔄 *Review* ({current}/{total})",
        "uz": "🔄 *Takrorlash* ({current}/{total})",
        "ru": "🔄 *Повторение* ({current}/{total})",
    },
    "review_complete": {
        "en": "🎉 *Review Complete!*\n\nYou reviewed {count} words.",
        "uz": "🎉 *Takrorlash yakunlandi!*\n\nSiz {count} ta so'zni takrorladingiz.",
        "ru": "🎉 *Повторение завершено!*\n\nВы повторили {count} слов.",
    },
    "session_expired": {
        "en": "Session expired. Please start a new review session.",
        "uz": "Sessiya muddati tugadi. Iltimos, yangi sessiya boshlang.",
        "ru": "Сессия истекла. Пожалуйста, начните новую сессию.",
    },
    
    # ============ Misc Messages ============
    "no_example": {
        "en": "No example available.",
        "uz": "Misol mavjud emas.",
        "ru": "Пример недоступен.",
    },
    "example_not_available": {
        "en": "Example not available",
        "uz": "Misol mavjud emas",
        "ru": "Пример недоступен",
    },
    "error_loading_word": {
        "en": "Error loading word",
        "uz": "So'zni yuklashda xatolik",
        "ru": "Ошибка загрузки слова",
    },
    "error_showing_answer": {
        "en": "Error showing answer",
        "uz": "Javobni ko'rsatishda xatolik",
        "ru": "Ошибка показа ответа",
    },
    "great_job": {
        "en": "✅ Great job!",
        "uz": "✅ Ajoyib!",
        "ru": "✅ Отлично!",
    },
    "btn_cancel": {
        "en": "❌ Cancel",
        "uz": "❌ Bekor qilish",
        "ru": "❌ Отмена",
    },
    
    # ============ Error Messages ============
    "error_no_words": {
        "en": "❌ No words found for Level {level} Unit {unit}.\n\nPlease check if the word data is available.",
        "uz": "❌ {level}-daraja {unit}-bo'lim uchun so'zlar topilmadi.\n\nIltimos, so'z ma'lumotlari mavjudligini tekshiring.",
        "ru": "❌ Слова для Уровня {level} Раздела {unit} не найдены.\n\nПожалуйста, проверьте наличие данных.",
    },
    "error_no_words_level": {
        "en": "❌ No words found for Level {level}.",
        "uz": "❌ {level}-daraja uchun so'zlar topilmadi.",
        "ru": "❌ Слова для Уровня {level} не найдены.",
    },
    "error_generic": {
        "en": "❌ Something went wrong. Please try again.",
        "uz": "❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.",
        "ru": "❌ Что-то пошло не так. Пожалуйста, попробуйте ещё раз.",
    },
    
    # ============ Test Section Extended ============
    "test_unit_select_level": {
        "en": "📝 *Unit Test*\n\nSelect a level:",
        "uz": "📝 *Bo'lim testi*\n\nDarajani tanlang:",
        "ru": "📝 *Тест по разделу*\n\nВыберите уровень:",
    },
    "test_level_unit_select": {
        "en": "📝 *Level {level} Unit Test*\n\nSelect a unit:",
        "uz": "📝 *{level}-daraja bo'lim testi*\n\nBo'limni tanlang:",
        "ru": "📝 *Тест по разделам Уровня {level}*\n\nВыберите раздел:",
    },
    "test_level_select": {
        "en": "📚 *Level Test*\n\n⚠️ This test covers ALL units in the level.\n\nSelect a level:",
        "uz": "📚 *Daraja testi*\n\n⚠️ Bu test darajadagi BARCHA bo'limlarni qamrab oladi.\n\nDarajani tanlang:",
        "ru": "📚 *Тест по уровню*\n\n⚠️ Этот тест охватывает ВСЕ разделы уровня.\n\nВыберите уровень:",
    },
    "test_generate_error": {
        "en": "❌ Could not generate test questions.",
        "uz": "❌ Test savollarini yaratib bo'lmadi.",
        "ru": "❌ Не удалось создать тестовые вопросы.",
    },
    "type_your_answer": {
        "en": "Type your answer:",
        "uz": "Javobingizni yozing:",
        "ru": "Введите ваш ответ:",
    },
    "no_weak_words": {
        "en": "✨ *No Weak Words!*\n\nGreat job! You don't have any weak words to review.\nKeep learning to add more words!",
        "uz": "✨ *Qiyin so'zlar yo'q!*\n\nAjoyib! Sizda takrorlash kerak bo'lgan qiyin so'zlar yo'q.\nYangi so'zlar o'rganishda davom eting!",
        "ru": "✨ *Нет сложных слов!*\n\nОтлично! У вас нет сложных слов для повторения.\nПродолжайте учить новые слова!",
    },
    "review_test_title": {
        "en": "🔄 *Review Test*",
        "uz": "🔄 *Takrorlash testi*",
        "ru": "🔄 *Тест на повторение*",
    },
    "custom_test_title": {
        "en": "✏️ *Custom Words Test*",
        "uz": "✏️ *Shaxsiy so'zlar testi*",
        "ru": "✏️ *Тест своих слов*",
    },
    "custom_test_no_words": {
        "en": "📝 *Not Enough Custom Words*\n\nYou need at least 4 custom words to start a test.\nGo to Learn → Add New Word to add your own words!",
        "uz": "📝 *Yetarli so'zlar yo'q*\n\nTest boshlash uchun kamida 4 ta shaxsiy so'z kerak.\nO'rganish → Yangi so'z qo'shish bo'limiga o'ting!",
        "ru": "📝 *Недостаточно слов*\n\nДля теста нужно минимум 4 слова.\nПерейдите в Учить → Добавить слово!",
    },
    "correct": {
        "en": "✅ Correct!",
        "uz": "✅ To'g'ri!",
        "ru": "✅ Правильно!",
    },
    "incorrect": {
        "en": "❌ Incorrect",
        "uz": "❌ Noto'g'ri",
        "ru": "❌ Неправильно",
    },
    "your_answer": {
        "en": "Your answer",
        "uz": "Sizning javobingiz",
        "ru": "Ваш ответ",
    },
    "correct_answer": {
        "en": "Correct answer",
        "uz": "To'g'ri javob",
        "ru": "Правильный ответ",
    },
    "the_word_is": {
        "en": "The word is",
        "uz": "So'z",
        "ru": "Слово",
    },
    "skipped": {
        "en": "Skipped",
        "uz": "O'tkazib yuborildi",
        "ru": "Пропущено",
    },
    "hint": {
        "en": "Hint",
        "uz": "Maslahat",
        "ru": "Подсказка",
    },
    "example": {
        "en": "Example",
        "uz": "Misol",
        "ru": "Пример",
    },
    "no_hint": {
        "en": "No hint available",
        "uz": "Maslahat mavjud emas",
        "ru": "Подсказка недоступна",
    },
    "test_ended": {
        "en": "Test ended.",
        "uz": "Test yakunlandi.",
        "ru": "Тест завершён.",
    },
    "coming_soon": {
        "en": "Coming soon!",
        "uz": "Tez orada!",
        "ru": "Скоро!",
    },
    "admin_only": {
        "en": "⛔ This command is for administrators only.",
        "uz": "⛔ Bu buyruq faqat administratorlar uchun.",
        "ru": "⛔ Эта команда только для администраторов.",
    },
    
    # ============ Test Results ============
    "test_question_progress": {
        "en": "📝 Question {current}/{total}",
        "uz": "📝 Savol {current}/{total}",
        "ru": "📝 Вопрос {current}/{total}",
    },
    "test_results_title": {
        "en": "📊 *Test Results*",
        "uz": "📊 *Test natijalari*",
        "ru": "📊 *Результаты теста*",
    },
    "test_details_title": {
        "en": "Test Details",
        "uz": "Test tafsilotlari",
        "ru": "Детали теста",
    },
    "no_test_details": {
        "en": "No test details available",
        "uz": "Test tafsilotlari mavjud emas",
        "ru": "Детали теста недоступны",
    },
    "correct_words": {
        "en": "Correct Words",
        "uz": "To'g'ri so'zlar",
        "ru": "Правильные слова",
    },
    "words_to_review": {
        "en": "Words to Review",
        "uz": "Takrorlash kerak so'zlar",
        "ru": "Слова для повторения",
    },
    "more": {
        "en": "more",
        "uz": "yana",
        "ru": "ещё",
    },
    "correct_count": {
        "en": "Correct",
        "uz": "To'g'ri",
        "ru": "Правильных",
    },
    "wrong_count": {
        "en": "Wrong",
        "uz": "Noto'g'ri",
        "ru": "Неправильных",
    },
    "score": {
        "en": "Score",
        "uz": "Ball",
        "ru": "Счёт",
    },
    "time": {
        "en": "Time",
        "uz": "Vaqt",
        "ru": "Время",
    },
    "min": {
        "en": "m",
        "uz": "d",
        "ru": "м",
    },
    "sec": {
        "en": "s",
        "uz": "s",
        "ru": "с",
    },
    "level": {
        "en": "Level",
        "uz": "Daraja",
        "ru": "Уровень",
    },
    "unit": {
        "en": "Unit",
        "uz": "Bo'lim",
        "ru": "Раздел",
    },
    "result_excellent": {
        "en": "🏆 Excellent! You've mastered these words!",
        "uz": "🏆 A'lo! Siz bu so'zlarni o'zlashtirdingiz!",
        "ru": "🏆 Отлично! Вы освоили эти слова!",
    },
    "result_great": {
        "en": "⭐ Great job! Keep up the good work!",
        "uz": "⭐ Ajoyib! Shu zaylda davom eting!",
        "ru": "⭐ Отлично! Продолжайте в том же духе!",
    },
    "result_good": {
        "en": "💪 Good effort! Keep practicing!",
        "uz": "💪 Yaxshi harakat! Mashq qilishda davom eting!",
        "ru": "💪 Хорошая работа! Продолжайте практиковаться!",
    },
    "result_keep_trying": {
        "en": "📚 Don't worry! Review these words and try again!",
        "uz": "📚 Xavotir olmang! Bu so'zlarni takrorlang va qaytadan urinib ko'ring!",
        "ru": "📚 Не переживайте! Повторите эти слова и попробуйте снова!",
    },
    
    # ============ Stats Section Extended ============
    "stats_words_progress": {
        "en": "Words Progress",
        "uz": "So'zlar taraqqiyoti",
        "ru": "Прогресс слов",
    },
    "learning": {
        "en": "Learning",
        "uz": "O'rganilmoqda",
        "ru": "Изучается",
    },
    "known": {
        "en": "Known",
        "uz": "Ma'lum",
        "ru": "Известно",
    },
    "mastered": {
        "en": "Mastered",
        "uz": "O'zlashtirilgan",
        "ru": "Освоено",
    },
    "need_review": {
        "en": "Need Review",
        "uz": "Takrorlash kerak",
        "ru": "Нужно повторить",
    },
    "activity": {
        "en": "Activity",
        "uz": "Faoliyat",
        "ru": "Активность",
    },
    "total_reviews": {
        "en": "Total Reviews",
        "uz": "Jami takrorlashlar",
        "ru": "Всего повторений",
    },
    "tests_taken": {
        "en": "Tests Taken",
        "uz": "Topshirilgan testlar",
        "ru": "Пройдено тестов",
    },
    "accuracy": {
        "en": "Accuracy",
        "uz": "Aniqlik",
        "ru": "Точность",
    },
    "streak": {
        "en": "Streak",
        "uz": "Seriya",
        "ru": "Серия",
    },
    "best_streak": {
        "en": "Best Streak",
        "uz": "Eng yaxshi seriya",
        "ru": "Лучшая серия",
    },
    "current": {
        "en": "Current",
        "uz": "Joriy",
        "ru": "Текущая",
    },
    "longest": {
        "en": "Longest",
        "uz": "Eng uzun",
        "ru": "Лучшая",
    },
    "days": {
        "en": "days",
        "uz": "kun",
        "ru": "дней",
    },
    "custom_words": {
        "en": "Custom Words",
        "uz": "Maxsus so'zlar",
        "ru": "Свои слова",
    },
    "progress": {
        "en": "Progress",
        "uz": "Taraqqiyot",
        "ru": "Прогресс",
    },
    "words_started": {
        "en": "Words Started",
        "uz": "Boshlangan so'zlar",
        "ru": "Начато слов",
    },
    "completed": {
        "en": "Completed",
        "uz": "Yakunlangan",
        "ru": "Завершено",
    },
    "in_progress": {
        "en": "In Progress",
        "uz": "Davom etmoqda",
        "ru": "В процессе",
    },
    "status": {
        "en": "Status",
        "uz": "Holat",
        "ru": "Статус",
    },
    "your_learning_streak": {
        "en": "Your Learning Streak",
        "uz": "O'rganish seriyangiz",
        "ru": "Ваша серия обучения",
    },
    "current_streak": {
        "en": "Current Streak",
        "uz": "Joriy seriya",
        "ru": "Текущая серия",
    },
    "longest_streak": {
        "en": "Longest Streak",
        "uz": "Eng uzun seriya",
        "ru": "Лучшая серия",
    },
    "streak_at_risk": {
        "en": "Streak at risk! Study now to keep your streak!",
        "uz": "Seriya xavf ostida! Seriyangizni saqlab qolish uchun hozir o'rganing!",
        "ru": "Серия под угрозой! Учитесь сейчас, чтобы сохранить серию!",
    },
    "streak_reset": {
        "en": "Your streak has reset. Start a new one today!",
        "uz": "Seriyangiz qayta boshlandi. Bugun yangisini boshlang!",
        "ru": "Ваша серия сброшена. Начните новую сегодня!",
    },
    "keep_it_up": {
        "en": "Keep it up! Study today to extend your streak!",
        "uz": "Shu zaylda davom eting! Seriyangizni uzaytirish uchun bugun o'rganing!",
        "ru": "Продолжайте! Учитесь сегодня, чтобы продлить серию!",
    },
    "start_streak": {
        "en": "Start your streak today! Learn some words now!",
        "uz": "Seriyangizni bugun boshlang! Hozir bir nechta so'z o'rganing!",
        "ru": "Начните серию сегодня! Выучите несколько слов сейчас!",
    },
    "streak_30_days": {
        "en": "Amazing! You're a vocabulary champion!",
        "uz": "Ajoyib! Siz lug'at chempionisiz!",
        "ru": "Потрясающе! Вы чемпион по словарному запасу!",
    },
    "streak_14_days": {
        "en": "Two weeks strong! You're unstoppable!",
        "uz": "Ikki hafta! Sizni to'xtata olmaydi!",
        "ru": "Две недели! Вас не остановить!",
    },
    "streak_7_days": {
        "en": "A whole week! Great consistency!",
        "uz": "Butun bir hafta! Ajoyib izchillik!",
        "ru": "Целая неделя! Отличное постоянство!",
    },
    "level_progress_title": {
        "en": "📘 *Level Progress*\n\nSelect a level to view progress:",
        "uz": "📘 *Daraja taraqqiyoti*\n\nTaraqqiyotni ko'rish uchun darajani tanlang:",
        "ru": "📘 *Прогресс по уровням*\n\nВыберите уровень для просмотра прогресса:",
    },
    "no_weak_words_stats": {
        "en": "✨ *Weak Words*\n\nGreat job! You don't have any weak words.\n\nKeep practicing to maintain your knowledge!",
        "uz": "✨ *Qiyin so'zlar*\n\nAjoyib! Sizda qiyin so'zlar yo'q.\n\nBilimingizni saqlab qolish uchun mashq qilishda davom eting!",
        "ru": "✨ *Сложные слова*\n\nОтлично! У вас нет сложных слов.\n\nПродолжайте практиковаться, чтобы поддерживать знания!",
    },
    "weak_words_summary": {
        "en": "⚠️ *Weak Words Summary*\n\nTotal weak words: *{count}*",
        "uz": "⚠️ *Qiyin so'zlar xulosasi*\n\nJami qiyin so'zlar: *{count}*",
        "ru": "⚠️ *Сводка по сложным словам*\n\nВсего сложных слов: *{count}*",
    },
    "weak_words_attention": {
        "en": "⚡ These words need your attention!\nConsider taking a review test.",
        "uz": "⚡ Bu so'zlar sizning e'tiboringizni talab qiladi!\nTakrorlash testini topshirishni o'ylab ko'ring.",
        "ru": "⚡ Эти слова требуют вашего внимания!\nРекомендуем пройти тест на повторение.",
    },
    
    # ============ Review Section Extended 2 ============
    "review_no_words_due": {
        "en": "🔄 *Review Mode*\n\n✨ You're all caught up!\n\nNo words are due for review right now.\nKeep learning new words or check back later!",
        "uz": "🔄 *Takrorlash rejimi*\n\n✨ Hammasi bajarildi!\n\nHozircha takrorlanadigan so'zlar yo'q.\nYangi so'zlar o'rganing yoki keyinroq qayting!",
        "ru": "🔄 *Режим повторения*\n\n✨ Всё повторено!\n\nСейчас нет слов для повторения.\nУчите новые слова или вернитесь позже!",
    },
    "review_words_due": {
        "en": "🔄 *Review Mode*\n\n📚 You have *{count}* words due for review!\n\nRegular review helps you remember words better.",
        "uz": "🔄 *Takrorlash rejimi*\n\n📚 Sizda takrorlash kerak bo'lgan *{count}* ta so'z bor!\n\nMuntazam takrorlash so'zlarni yaxshiroq eslab qolishga yordam beradi.",
        "ru": "🔄 *Режим повторения*\n\n📚 У вас *{count}* слов для повторения!\n\nРегулярное повторение помогает лучше запоминать слова.",
    },
    "review_no_words_due_short": {
        "en": "🔄 *Review Mode*\n\n✨ You're all caught up!\nNo words due for review.",
        "uz": "🔄 *Takrorlash rejimi*\n\n✨ Hammasi bajarildi!\nTakrorlanadigan so'zlar yo'q.",
        "ru": "🔄 *Режим повторения*\n\n✨ Всё повторено!\nНет слов для повторения.",
    },
    "review_words_due_short": {
        "en": "🔄 *Review Mode*\n\n📚 *{count}* words due for review",
        "uz": "🔄 *Takrorlash rejimi*\n\n📚 *{count}* so'z takrorlash kerak",
        "ru": "🔄 *Режим повторения*\n\n📚 *{count}* слов для повторения",
    },
    "no_weak_words_review": {
        "en": "⚠️ *Weak Words*\n\n✨ Great news! You don't have any weak words.\n\nKeep practicing to maintain your knowledge!",
        "uz": "⚠️ *Qiyin so'zlar*\n\n✨ Ajoyib yangilik! Sizda qiyin so'zlar yo'q.\n\nBilimingizni saqlab qolish uchun mashq qilishda davom eting!",
        "ru": "⚠️ *Сложные слова*\n\n✨ Отлично! У вас нет сложных слов.\n\nПродолжайте практиковаться, чтобы поддерживать знания!",
    },
    "weak_words_list": {
        "en": "⚠️ *Weak Words* ({count} total)\n\nThese words need more practice:\n\n{word_list}\n{more}\n\nTake a review test to practice them!",
        "uz": "⚠️ *Qiyin so'zlar* (jami {count})\n\nBu so'zlar ko'proq mashq talab qiladi:\n\n{word_list}\n{more}\n\nUlarni mashq qilish uchun takrorlash testini toping!",
        "ru": "⚠️ *Сложные слова* (всего {count})\n\nЭти слова требуют больше практики:\n\n{word_list}\n{more}\n\nПройдите тест на повторение!",
    },
    "review_schedule_title": {
        "en": "📅 *Review Schedule (7 Days)*",
        "uz": "📅 *Takrorlash jadvali (7 kun)*",
        "ru": "📅 *Расписание повторения (7 дней)*",
    },
    "review_schedule_tip": {
        "en": "Regular review helps you remember!",
        "uz": "Muntazam takrorlash eslab qolishga yordam beradi!",
        "ru": "Регулярное повторение помогает запоминать!",
    },
    
    # ============ 4000 Words Section ============
    "4000_words_title": {
        "en": "📘 *4000 Essential English Words*\n\nMaster vocabulary across 6 levels, from beginner to advanced.\n\n• 6 Levels\n• 30 Units per level\n• ~20 Words per unit\n\nWhat would you like to do?",
        "uz": "📘 *4000 muhim inglizcha so'zlar*\n\nBoshlang'ich darajadan ilg'orgacha 6 darajali lug'atni o'rganing.\n\n• 6 daraja\n• Har darajada 30 bo'lim\n• Har bo'limda ~20 so'z\n\nNima qilmoqchisiz?",
        "ru": "📘 *4000 важных английских слов*\n\nОсвойте словарный запас на 6 уровнях, от начального до продвинутого.\n\n• 6 уровней\n• 30 разделов на уровень\n• ~20 слов на раздел\n\nЧто вы хотите сделать?",
    },
    "4000_words_menu": {
        "en": "📘 *4000 Essential English Words*\n\nWhat would you like to do?",
        "uz": "📘 *4000 muhim inglizcha so'zlar*\n\nNima qilmoqchisiz?",
        "ru": "📘 *4000 важных английских слов*\n\nЧто вы хотите сделать?",
    },
    "4000_essential_words": {
        "en": "4000 Essential Words",
        "uz": "4000 muhim so'z",
        "ru": "4000 важных слов",
    },
    "btn_browse_levels": {
        "en": "📖 Browse Levels",
        "uz": "📖 Darajalarni ko'rish",
        "ru": "📖 Просмотр уровней",
    },
    "btn_continue_learning": {
        "en": "▶️ Continue Learning",
        "uz": "▶️ O'rganishni davom ettirish",
        "ru": "▶️ Продолжить обучение",
    },
    "btn_take_test": {
        "en": "📝 Take Test",
        "uz": "📝 Test topshirish",
        "ru": "📝 Пройти тест",
    },
    "btn_my_progress": {
        "en": "📊 My Progress",
        "uz": "📊 Mening progressim",
        "ru": "📊 Мой прогресс",
    },
    "level": {
        "en": "Level",
        "uz": "Daraja",
        "ru": "Уровень",
    },
    "unit": {
        "en": "Unit",
        "uz": "Bo'lim",
        "ru": "Раздел",
    },
    "progress": {
        "en": "Progress",
        "uz": "Progress",
        "ru": "Прогресс",
    },
    "learned": {
        "en": "Learned",
        "uz": "O'rganilgan",
        "ru": "Изучено",
    },
    "mastered": {
        "en": "Mastered",
        "uz": "O'zlashtirilgan",
        "ru": "Освоено",
    },
    "weak": {
        "en": "Weak",
        "uz": "Qiyin",
        "ru": "Слабые",
    },
    "select_unit": {
        "en": "Select a unit",
        "uz": "Bo'limni tanlang",
        "ru": "Выберите раздел",
    },
    "words": {
        "en": "Words",
        "uz": "So'zlar",
        "ru": "Слова",
    },
    "known": {
        "en": "Known",
        "uz": "Ma'lum",
        "ru": "Знакомые",
    },
    "words_in_unit": {
        "en": "Words in this unit",
        "uz": "Bu bo'limdagi so'zlar",
        "ru": "Слова в этом разделе",
    },
    "and_more": {
        "en": "...and {count} more",
        "uz": "...va yana {count} ta",
        "ru": "...и ещё {count}",
    },
    "error_no_words": {
        "en": "❌ No words found for Level {level} Unit {unit}.\n\nThe word data may not be loaded yet.",
        "uz": "❌ {level}-daraja {unit}-bo'lim uchun so'zlar topilmadi.\n\nSo'z ma'lumotlari hali yuklanmagan bo'lishi mumkin.",
        "ru": "❌ Слова для Уровня {level} Раздела {unit} не найдены.\n\nДанные могут быть ещё не загружены.",
    },
    "continue_learning": {
        "en": "📖 *Continue Learning*\n\nYou're currently on:\n📘 Level {level} • Unit {unit}\n\nReady to continue?",
        "uz": "📖 *O'rganishni davom ettirish*\n\nSiz hozirda:\n📘 {level}-daraja • {unit}-bo'lim\n\nDavom etishga tayyormisiz?",
        "ru": "📖 *Продолжить обучение*\n\nВы сейчас на:\n📘 Уровень {level} • Раздел {unit}\n\nГотовы продолжить?",
    },
    "4000_test_title": {
        "en": "📝 *4000 Words Test*\n\nChoose a test type:",
        "uz": "📝 *4000 so'z testi*\n\nTest turini tanlang:",
        "ru": "📝 *Тест 4000 слов*\n\nВыберите тип теста:",
    },
    "4000_progress_title": {
        "en": "4000 Words Progress",
        "uz": "4000 so'z progressi",
        "ru": "Прогресс 4000 слов",
    },
    "overall": {
        "en": "Overall",
        "uz": "Umumiy",
        "ru": "Общий",
    },
}


def get_text(key: str, lang: str = DEFAULT_LANGUAGE, **kwargs) -> str:
    """
    Get localized text by key
    
    Args:
        key: Text key from TEXTS dictionary
        lang: Language code (en, uz, ru)
        **kwargs: Format arguments for the text
    
    Returns:
        Localized text string
    """
    if key not in TEXTS:
        return f"[Missing: {key}]"
    
    text = TEXTS[key].get(lang, TEXTS[key].get(DEFAULT_LANGUAGE, f"[Missing: {key}]"))
    
    if kwargs:
        try:
            return text.format(**kwargs)
        except KeyError:
            return text
    
    return text


def get_language_name(lang_code: str) -> str:
    """Get display name for a language code"""
    return LANGUAGES.get(lang_code, LANGUAGES[DEFAULT_LANGUAGE])


def get_available_languages() -> dict:
    """Get all available languages"""
    return LANGUAGES.copy()
