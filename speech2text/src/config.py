from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    class Config:
        env_file = ".env"
        extra = "ignore"


class NLPConfig(BaseConfig):
    model_config = SettingsConfigDict(env_prefix="NLP_")

    token: str
    model: str


class LABSConfig(BaseConfig):
    model_config = SettingsConfigDict(env_prefix="LABS_")

    api_key: str