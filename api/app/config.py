from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str="postgresql+asyncpg://postgres:postgres@localhost:5432/taskforge"
    REDIS_URL: str="redis://localhost:6379/0"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8"
    }

settings = Settings()