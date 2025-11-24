import logging
from pathlib import Path
from functools import wraps

from googleapiclient.http import MediaIoBaseDownload

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from speech2text.src.models import AudioFile
from speech2text.src.config import GoogleDriveConfig


LOGGER: logging.Logger = logging.getLogger('GoogleDriveAPI')


class GoogleDriveAPIError(HttpError): ...


def handle_http_errors(func):
    """
    Отлавливаем HTTP ошибки (и прокидываем свою по желанию)
        так же можно реализовать эту логику в __exit__,
        но, по желанию, можно возвращать None в случае ошибки
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.service is None:
            LOGGER.critical('Сервис для работы с Google Drive не инициализирован')
            raise GoogleDriveAPIError

        try:
            return func(self, *args, **kwargs)
        except HttpError:
            LOGGER.exception(f'Произошла ошибка в {func.__name__}')
            raise GoogleDriveAPIError
            # return None
        except Exception:
            LOGGER.exception(f'Произошла неожиданная ошибка в {func.__name__}')

    return wrapper


class GoogleDriveAPI:
    """
    Класс для работы с Google Drive API
    """

    # drive
    # drive.readonly
    # drive.metadata.readonly
    URL = 'https://www.googleapis.com/auth/'

    FOLDER_ID = GoogleDriveConfig().folder_id

    def __init__(self, *, scopes: list[str]):
        self.creds: Credentials | None = None
        self.service = None # Drive API Client
        self.scopes = [GoogleDriveAPI.URL + scope for scope in scopes]

    def __enter__(self):
        self._get_creds()   # Проверяем токены
        LOGGER.info('Токены успешно загружены')
        self.service = build("drive", "v3", credentials=self.creds)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        ...

    def _get_creds(self):
        # TODO: хранить токены в БД

        # Файл tokes.json хранит в себе access и refresh токены
        # создается автоматически после первой авторизации
        self.creds = Credentials.from_authorized_user_file('token.json', self.scopes) \
            if Path('token.json').exists() else None

        # Если их нет или они не валидны - аутентификация
        if not self.creds or not self.creds.valid:

            # Если наш токен истек, пробуем его обновить
            if self.creds and self.creds.expired and self.creds.refresh_token:
                LOGGER.info('Токен устарел, обновляю...')
                self.creds.refresh(Request())

            # Если токенов нет вообще или мы не можем его обновить
            # запускаем авторизацию
            else:
                LOGGER.info('Необходима авторизация')
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.scopes
                )
                self.creds = flow.run_local_server(port=0)

            # Сохраняем токены в token.json
            Path('token.json').write_text(self.creds.to_json())

    @handle_http_errors
    def get_all_audio(self) -> list[AudioFile]:
        """
        Получаем все аудиофайлы из папки audio/
        :return:
            list[AudioFile]
        """

        audio_files: list[dict[str, str]] = []
        page_token = None
        query = (
            f'"{GoogleDriveAPI.FOLDER_ID}" in parents and '
            'mimeType contains "audio/" and '
            'trashed = false'
        )

        while True:
            response = self.service.files().list(
                q=query,
                fields="nextPageToken, files(id, name, mimeType)",
                pageSize=100,
                pageToken=page_token,
            ).execute()

            audio_files.extend(response.get("files", []))
            page_token = response.get("nextPageToken", None)

            if page_token is None:
                break

        return [AudioFile(**item) for item in audio_files]

    @handle_http_errors
    def download_audio(self, file: AudioFile, destination: Path):
        """
        Скачиваем файл в папку
        """
        requests = self.service.files().get_media(fileId=file.id)

        with destination.open('wb') as f:
            downloader = MediaIoBaseDownload(f, requests)

            is_done = False
            while not is_done:
                _, is_done = downloader.next_chunk()

            LOGGER.info(f'Файл {file.name} успешно скачан')