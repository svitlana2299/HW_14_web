import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from jose import jwt
from passlib.context import CryptContext

from app.main import app
from app.config import settings
from app.models import Base, User
from app.crud import create_user
from app.auth import create_access_token

# Створюємо інтерфейс для тестування API
client = TestClient(app)

# Створюємо з'єднання з тестовою базою даних та сесію SQLAlchemy
DATABASE_URL = settings.database_url
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

# Встановлюємо з'єднання з базою даних перед тестами та видаляємо її після них


@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal()
    yield session
    session.close()
    transaction.rollback()
    connection.close()

# Тест для створення та аутентифікації користувача


def test_create_and_authenticate_user(db_session):
    user_data = {"email": "test@example.com", "password": "testpassword"}
    user = create_user(db_session, user_data["email"], user_data["password"])

    response = client.post(
        "/login/access-token", data={"username": user_data["email"], "password": user_data["password"]})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    token = data["access_token"]

    decoded_data = jwt.decode(
        token, settings.secret_key, algorithms=[settings.algorithm])
    assert decoded_data["sub"] == user.email

# Тест для перевірки авторизації користувача


def test_authorize_user(db_session):
    user_data = {"email": "test@example.com", "password": "testpassword"}
    user = create_user(db_session, user_data["email"], user_data["password"])

    token = create_access_token(data={"sub": user.email})

    response = client.get(
        "/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert "email" in data
    assert data["email"] == user.email
