import logging
from pathlib import Path

from speech2text.src import (
    GoogleDriveAPI,
    ElevenLabsClient,
    GeminiClient,
)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
LOGGER = logging.getLogger(__name__)

# Папка с записями
FOLDER = Path('audio')


def load_from_google_drive():
    """
    Загружаем записи из Google Drive
    """
    # ??? по желанию можем обработать GoogleDriveAPIError

    # Прав на чтение нам хватит для скачивания файла
    scopes = ['drive.readonly']

    # ID папки audio/ на Google Drive (можно посмотреть через браузер в ссылке)
    folder_id = '1LKZSb8Z2ZFQGXffoitNpDytiSgA4GT0C'

    with GoogleDriveAPI(scopes=scopes) as api:
        # Получаем файлы из Google Drive
        files = api.get_all_audio(folder_id)

        for audio in files:

            # Если записи разговора нет, скачиваем её
            dst = FOLDER / audio.name
            if not dst.exists():
                api.download_audio(audio, dst)

def load_transcription():
    """
    Создаем файли транскрипции
    """
    # Пробовал NLP Cloud
    # nlp = NLPClient()
    # file = FOLDER / '2024-11-13_12-57_0667131186_outgoing.mp3'
    # response = nlp.transcribe(file)
    # print(response)

    labs = ElevenLabsClient()

    for audio_file in FOLDER.iterdir():
        dst = audio_file.with_suffix('.txt')

        # Если текст разговора уже существует, идем дальше
        if dst.exists():
            continue

        text = labs.transcribe(audio_file)
        dst.write_text(text, encoding='utf-8')
        LOGGER.info(f'File {audio_file.name} is done')

def rate_audio():
    gemini = GeminiClient()
    files = (f for f in FOLDER.iterdir() if f.suffix == '.txt')

    for file in files:
        content = file.read_text(encoding='utf-8')
        result = gemini.analyze_dialogue(content)
        print(result)

        break

def main():
    load_from_google_drive()
    load_transcription()
    rate_audio()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Ctrl+C")