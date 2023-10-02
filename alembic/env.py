from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Імпортуємо ваші моделі та інші файли
from app.models import Base
from app.config import settings  # Імпортуємо налаштування

# Імпортуємо вашу базу даних
from sqlalchemy import create_engine

# Використовуємо налаштування для URL бази даних
DATABASE_URL = settings.database_url
engine = create_engine(DATABASE_URL)

# Використовуємо модель бази даних, яку ви визначили у вашому проекті
target_metadata = Base.metadata

# Цей блок конфігурації служить для налаштування Alembic
config = context.config

# З'єднуємося з базою даних
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Підказуємо Alembic, як знаходити моделі та об'єкти бази даних
config.set_main_option("script_location", "your_project")

# Ваші налаштування слухачів або інші налаштування Alembic можна додати тут

# Залишимо цей рядок коду, який дозволяє Alembic визначити вашу модель бази даних
# і створити необхідні SQL-запити для міграції


def run_migrations_online():
    # Звідси розпочинаємо з'єднання з базою даних
    with context.begin_transaction():
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()
