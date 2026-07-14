from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    cassandra_host: str = "localhost"
    cassandra_port: int = 9043
    cassandra_keyspace: str = "shrinkr"
    app_host: str = "127.0.0.1"
    app_port: int = 8000


@lru_cache
def settings() -> Settings:
    return Settings()