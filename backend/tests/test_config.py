from app.core.config import Settings


def test_local_settings_default_to_sqlite() -> None:
    settings = Settings()
    assert settings.resolved_database_url.startswith("sqlite:///")


def test_production_database_url_is_built_from_components() -> None:
    settings = Settings(
        database_host="db.example.internal",
        database_user="clinicflow",
        database_password="p@ss word",
        database_name="clinicflow",
        database_port=5432,
    )
    assert settings.resolved_database_url == (
        "postgresql+psycopg://clinicflow:p%40ss+word@db.example.internal:5432/clinicflow"
    )
