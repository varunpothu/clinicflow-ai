from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ClinicFlow AI"
    app_env: str = "local"
    log_level: str = "INFO"
    database_url: str = "sqlite:///./clinicflow.db"
    clinic_timezone: str = "Europe/London"
    ai_provider: str = "mock"
    aws_region: str = "eu-west-2"
    bedrock_model_id: str | None = None
    bedrock_guardrail_identifier: str | None = None
    bedrock_guardrail_version: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
