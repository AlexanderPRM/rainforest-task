"""Module with Project configuration."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class RelationalDatabaseSettings(BaseSettings):
    """Relational Database Configuration."""

    model_config = SettingsConfigDict(extra='ignore', case_sensitive=True, env_prefix='DB_')

    DRIVER: str
    HOST: str
    PORT: int
    USER: str
    PASSWORD: str
    NAME: str
    SCHEMA: str
