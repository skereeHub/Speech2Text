from pydantic import BaseModel


class AudioFile(BaseModel):
    id: str
    name: str
    mimeType: str