from logging import config as logging_config
from pathlib import Path

from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, RedisDsn, validator

from .logger import LOGGING_CONFIG

logging_config.dictConfig(LOGGING_CONFIG)

BASE_DIR = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    """Settings class to read environment variables."""

    project_name: str
    secret_key: str
    request_limit_per_minute: int

    postgres_dsn: PostgresDsn
    redis_dsn: RedisDsn
    jaeger_dsn: AnyHttpUrl

    jwt_secret_key: str
    access_token_expires: int
    refresh_token_expires: int

    client_secrets_file: Path | str
    scopes: list[str] | str

    @validator('client_secrets_file', pre=True, always=True)
    def set_secret_file_path(cls, v: Path | str) -> Path | str:
        """Set absolute path to client secret file."""

        return BASE_DIR / f'auth/{v}'

    @validator('scopes', pre=True, always=True)
    def set_scopes(cls, v: list[str] | str) -> list[str]:
        """Set scopes values as a list."""

        if isinstance(v, str):
            return v.split(' ')
        return v

    class Config:
        env_file = BASE_DIR / '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
