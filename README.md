### ТЗ:
1) Завантажити аудіофайли з Google Drive на локальному диску.
2) Отримати текст з файлу діалогу.
3) Проаналізувати текст на перелік відповідностей та надати оцінку менеджера

### Що є на цей час:
* [x] Завантаження аудіофайлів з Google Drive.
* [x] Отримання тексту з аудіо (Speech-to-text)
* [ ] Аналіз діалогу з клієнтом

### Залежності:
- Python >=3.11
- Google Cloud API
- ElevenLabs API

### Налаштування IDE:
1) `poetry install`

### Налаштування Google Cloud (для Google Drive API):
1) Перейти на [Google Cloud](https://console.cloud.google.com/);
2) Створити проєкт або обрати існуючий;
3) Увімкнути [Google Drive API](https://console.cloud.google.com/apis/library/drive.googleapis.com)
4) Створити [credentials](https://console.cloud.google.com/apis/credentials)
    1. Create credentials -> OAuth client ID -> Desktop app -> Create
    2. З'явиться вікно з даними для входу, тиснемо Download JSON та зберігаємо у корені проєкту під назвою `credentials.json`
5) (???) У функції `main.py load_from_google_drive()` вказуємо ID папки `audio/`
6) При першому запуску скрипт відкриє вікно авторизації Google для отримання токенів. Вони зберігаються у файлі `token.json`

### Налаштування ElevenLabs (для speech-to-text)
1) Перейти на [ElevenLabs](https://elevenlabs.io/app/developers)
2) API Keys -> Create Key -> Speach to Text Enabled
3) Ключ вставляємо в .env (див. .env.example)


### TODO:
* [ ] аналіз тексту
* [ ] сховати google creds в .env файл
* [ ] прокинути folder_id у .env файл
* [ ] налаштувати logging
