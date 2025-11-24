from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    class Config:
        env_file = ".env"
        extra = "ignore"


class GoogleDriveConfig(BaseConfig):
    """
    Для Google Drive
    """
    model_config = SettingsConfigDict(env_prefix="DRIVE_")

    folder_id: str


class LABSConfig(BaseConfig):
    """
    Для ElevenLabs
    """
    model_config = SettingsConfigDict(env_prefix="LABS_")

    api_key: str


class GeminiConfig(BaseConfig):
    """
    Дл Gemini
    """
    model_config = SettingsConfigDict(env_prefix="GEMINI_")

    api_key: str