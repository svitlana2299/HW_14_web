# Додаток для керування контактами

Цей додаток створено для керування контактами. Ви можете додавати, редагувати, видаляти та шукати контакти в базі даних. Додаток створено з використанням Python, FastAPI, SQLAlchemy і багатьох інших бібліотек.

## Вимоги

Перед початком роботи переконайтеся, що у вас встановлені такі програми і пакети:

- Python 3.8 або вище
- Docker та Docker Compose (якщо ви плануєте використовувати Docker)

## Встановлення

1. Склонуйте цей репозиторій на свій локальний комп'ютер:

   ```bash
   git clone https://github.com/yourusername/contact-manager-app.git
   cd contact-manager-app
Створіть файл оточення .env та налаштуйте його. Зразок .env файлу:
DATABASE_URL=postgresql://svitlana:2299@localhost/contact_manager_db
SECRET_KEY=mysecretkey
ALGORITHM=HS256
ALLOWED_ORIGINS=http://localhost,http://example.com
# Додайте інші змінні середовища за потребою
Запустіть додаток:

Якщо ви використовуєте Docker, запустіть команду:

docker-compose up --build
Якщо ви не використовуєте Docker, встановіть залежності з requirements.txt і запустіть додаток згідно до інструкцій у вашому середовищі.

Використання
Після запуску додатку ви можете відкрити його у вашому веб-браузері або використовувати API для взаємодії з додатком.
Документація API доступна за адресою http://localhost/docs.
Розробка
Якщо ви хочете внести зміни або вдосконалити цей додаток, ось деякі кроки для розробки:

Створіть віртуальне середовище і активуйте його:
Якщо ви не використовуєте Docker, встановіть залежності з requirements.txt і запустіть додаток згідно до інструкцій у вашому середовищі.

Використання
Після запуску додатку ви можете відкрити його у вашому веб-браузері або використовувати API для взаємодії з додатком.
Документація API доступна за адресою http://localhost/docs.
Розробка
Якщо ви хочете внести зміни або вдосконалити цей додаток, ось деякі кроки для розробки:

Створіть віртуальне середовище і активуйте його:
python -m venv venv
source venv/bin/activate

Встановіть залежності з requirements.txt:
pip install -r requirements.txt

Запустіть додаток у режимі розробки:
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

Додаток має набір тестів для перевірки його функціональності. Ви можете запустити тести за допомогою pytest:
pytest