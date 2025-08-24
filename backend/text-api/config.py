from pydantic_settings import BaseSettings, SettingsConfigDict


class Configuration(BaseSettings):
    max_file_size: int
    file_upload_dir: str
    default_llm_provider: str
    default_llm_model: str
    llm_provider_url: str
    logging_level: str = "INFO"
    model_config = SettingsConfigDict(env_file=".env")