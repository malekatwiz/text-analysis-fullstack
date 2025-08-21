from pydantic_settings import BaseSettings, SettingsConfigDict


class Configuration(BaseSettings):
    max_file_size: int
    file_upload_dir: str
    model_config = SettingsConfigDict(env_file=".env")