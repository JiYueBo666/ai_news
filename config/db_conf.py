from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ASYNC_DATABASE_URL: str = ""
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()

async_engine = create_async_engine(
    url=settings.ASYNC_DATABASE_URL, echo=True, pool_size=10, max_overflow=20
)


AsyncSessionLocal = async_sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            pass
