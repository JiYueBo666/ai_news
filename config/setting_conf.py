from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ASYNC_DATABASE_URL: str = ""
    REDIS_HOST: str = ""
    REDIS_PORT: int = 6379
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
