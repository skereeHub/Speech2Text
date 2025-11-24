### ТЗ:
1) Завантажити аудіофайли з Google Drive на локальному диску.
2) Отримати текст з файлу діалогу.
3) Проаналізувати текст на перелік відповідностей та надати оцінку менеджера
4) Зберегти результат в Excel таблицю

### Що є на цей час:
* [x] Завантаження аудіофайлів з Google Drive.
* [x] Отримання тексту з аудіо (Speech-to-text)
* [x] Аналіз діалогу з клієнтом
* [x] Збереження результатів в Excel файл

### Залежності:
- Python >=3.11
- Google Cloud API
- ElevenLabs API
- Gemini API

### Налаштування IDE:
1) `poetry install`
2) Копіюємо `Звіт прослуханих розмов.xlsx` у корінь проєкту

### Налаштування Google Cloud (для Google Drive API):
1) Перейти на [Google Cloud](https://console.cloud.google.com/);
2) Створити проєкт або обрати існуючий;
3) Увімкнути [Google Drive API](https://console.cloud.google.com/apis/library/drive.googleapis.com)
4) Створити [credentials](https://console.cloud.google.com/apis/credentials)
    1. Create credentials -> OAuth client ID -> Desktop app -> Create
    2. З'явиться вікно з даними для входу, тиснемо Download JSON та зберігаємо у корені проєкту під назвою `credentials.json`
5) Зберегти ID папки `audio/` в .env (див. .env.example)
6) При першому запуску скрипт відкриє вікно авторизації Google для отримання токенів. Вони зберігаються у файлі `token.json`

### Налаштування ElevenLabs (для speech-to-text)
1) Перейти на [ElevenLabs](https://elevenlabs.io/app/developers)
2) API Keys -> Create Key -> Speach to Text Enabled
3) Зберегти ключ в .env (див. .env.example)

### Налаштування Gemini API (для аналізу тексту)
1) Перейти на [Google AI Studio](https://aistudio.google.com/app/api-keys)
2) Create API Key
3) Зберегти ключ в .env (див. .env.example)

### Запуск:
```cmd
py main.py
```

### Зауваження:
- Наразі це мінімально робоче рішення
- Таблиця заповнюється починаючи з 1342 рядку, тому що з'явились складнощі з пошуком останнього порожнього рядка.
- Немає асинхронності/багатопоточності
- Усі логи виводяться в консоль

### TODO:
* [x] аналіз тексту
* [x] розширити можливості аналізу
* [x] зберегти результат аналізу в excel таблицю
* [ ] сховати google creds
* [x] прокинути folder_id у .env файл
* [ ] налаштувати logging
* [ ] обробити можливі помилки
* [ ] рефакторинг коду
