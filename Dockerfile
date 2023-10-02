# Використовуємо офіційний образ Python 3.8 від Docker Hub
FROM python:3.8

# Встановлюємо змінну середовища для Python, щоб вимкнути буферизацію виводу
ENV PYTHONUNBUFFERED 1

# Встановлюємо основні залежності
RUN pip install --no-cache-dir fastapi uvicorn sqlalchemy psycopg2-binary python-jose passlib

# Створюємо робочу директорію для нашого додатку
WORKDIR /app

# Копіюємо файли з додатку в контейнер
COPY ./app /app

# Встановлюємо gunicorn, якщо потрібно для продакшн-режиму
# RUN pip install gunicorn

# Встановлюємо alembic для керування міграціями бази даних
# RUN pip install alembic

# Встановлюємо Redis, якщо потрібно для кешування
# RUN apt-get update && apt-get install -y redis-server

# Відкриваємо порт для зовнішніх запитів
EXPOSE 80

# Запускаємо додаток за допомогою Uvicorn при запуску контейнера
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
