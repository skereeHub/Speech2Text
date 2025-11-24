from pathlib import Path

from elevenlabs.client import ElevenLabs

from speech2text.src.config import LABSConfig
from speech2text.src.utils import benchmark


class ElevenLabsClient:
    """
    Клиент для работы с ElevenLabs API (https://elevenlabs.io/docs/overview)
    """

    def __init__(self):
        self.client = ElevenLabs(api_key=LABSConfig().api_key)

    @benchmark
    def transcribe(self, audio: Path) -> str:
        b = audio.read_bytes()
        response = self.client.speech_to_text.convert(
            file=b,
            model_id='scribe_v1',
            tag_audio_events=True,
            language_code='ukr',
            diarize=True,
        )
        return response.text