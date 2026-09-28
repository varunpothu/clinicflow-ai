from functools import lru_cache
from urllib.parse import quote_plus

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ClinicFlow AI"
    app_env: str = "local"
    log_level: str = "INFO"
    database_url: str | None = None
    database_host: str | None = None
    database_port: int = 5432
    database_name: str = "clinicflow"
    database_user: str | None = None
    database_password: str | None = None
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

    @property
    def resolved_database_url(self) -> str:
        if self.database_url:
            return self.database_url
        if not self.database_host or not self.database_user or not self.database_password:
            return "sqlite:///./clinicflow.db"
        user = quote_plus(self.database_user)
        password = quote_plus(self.database_password)
        return (
            f"postgresql+psycopg://{user}:{password}@"
            f"{self.database_host}:{self.database_port}/{self.database_name}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
