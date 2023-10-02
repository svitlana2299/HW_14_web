from pydantic import BaseSettings


class Settings(BaseSettings):
    # Налаштування бази даних
    database_url: str = "postgresql://svitlana:2299@localhost/contact_manager_db"

    # Секретний ключ для генерації JWT токенів
    secret_key: str = "your-secret-key"

    # Тривалість дії JWT токену
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"  # Завантажуємо налаштування з файлу .env


settings = Settings()
