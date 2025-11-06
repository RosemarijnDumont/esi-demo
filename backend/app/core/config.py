
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
import os


class Settings(BaseSettings):
    # Database settings
    DATABASE_HOST: str
    DATABASE_PORT: int = 5432
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DB_STATEMENT_TIMEOUT_MS: int = 300000  # 5 minutes

    # Read Replica settings (optional)
    READ_REPLICA_HOST: str = ""
    READ_REPLICA_PORT: int = 5432
    READ_REPLICA_NAME: str = ""
    READ_REPLICA_USER: str = ""
    READ_REPLICA_PASSWORD: str = ""

    # Celery settings
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    # Export settings
    EXPORT_BATCH_SIZE: int = 50000  # Number of records to fetch per database query
    EXPORT_FILE_DIR: Path = Path("./exports") # Directory to save exported files

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()

