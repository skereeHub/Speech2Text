import logging
from pathlib import Path

from speech2text.src import (
    GoogleDriveConfig,
    GoogleDriveAPI,
    ElevenLabsClient,
    GeminiClient,
    Report,
    date_from_filename,
    Excel,
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

    with GoogleDriveAPI(scopes=scopes) as api:
        # Получаем файлы из Google Drive
        files = api.get_all_audio(GoogleDriveConfig().folder_id)

        for audio in files:

            # Если записи разговора нет, скачиваем её
            dst = FOLDER / audio.name
            if not dst.exists():
                api.download_audio(audio, dst)

def load_transcription():
    """
    Создаем текстовые файлы
    """
    labs = ElevenLabsClient()

    for audio_file in FOLDER.iterdir():
        dst = audio_file.with_suffix('.txt')

        # Если текст разговора уже существует, идем дальше
        if dst.exists():
            continue

        text = labs.transcribe(audio_file)
        dst.write_text(text, encoding='utf-8')
        LOGGER.info(f'File {audio_file.name} is done')

def analyzing_audio():
    """
    Отдаём текст Gemini, записываем результат в Excel таблицу
    """
    gemini = GeminiClient()
    files = (f for f in FOLDER.iterdir() if f.suffix == '.txt')

    with Excel() as excel:
        for file in files:
            content = file.read_text(encoding='utf-8')
            report = gemini.analyze_dialogue(content)
            report['date'] = date_from_filename(file.stem)
            report = Report(**report)
            excel.write_report(report)
            LOGGER.info(f'Report for {file.stem} is done')

def main():
    load_from_google_drive()
    load_transcription()
    analyzing_audio()
    LOGGER.info('DONE')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Ctrl+C")