import base64
from pathlib import Path

import nlpcloud

from speech2text.src.config import NLPConfig
from speech2text.src.utils import benchmark


class NLPClient:
    """
    Клиент для работы с NLP Cloud (https://nlpcloud.com/)
        бесплатно предоставляет API для работы с Whisper,
        но с ограничениями по продолжительности файла (до 200 секунд)
    """
    def __init__(self):
        self.config = NLPConfig()
        self.client = nlpcloud.Client(
            **self.config.model_dump(),
            gpu=True
        )

    @benchmark
    def transcribe(self, audio: Path) -> str | None:
        b = audio.read_bytes()
        b = base64.b64encode(b).decode('utf-8')
        response = self.client.asr(encoded_file=b)
        return response.get('text')