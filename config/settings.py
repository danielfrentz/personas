from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ollama_model: str

    model_config = SettingsConfigDict(env_file="settings.env", extra="ignore")
