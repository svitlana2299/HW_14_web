import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.config import settings
from app.models import Base
from app.crud import create_contact, get_contact, update_contact, delete_contact
from app.schemas import ContactCreate, ContactUpdate

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

# Тест для створення контакта


def test_create_contact(db_session):
    contact_data = {"name": "John", "surname": "Doe",
                    "email": "john.doe@example.com"}
    contact_create = ContactCreate(**contact_data)
    created_contact = create_contact(db_session, contact_create)
    assert created_contact is not None
    assert created_contact.name == contact_data["name"]
    assert created_contact.surname == contact_data["surname"]
    assert created_contact.email == contact_data["email"]

# Тест для отримання контакта за ідентифікатором


def test_get_contact(db_session):
    contact_data = {"name": "John", "surname": "Doe",
                    "email": "john.doe@example.com"}
    contact_create = ContactCreate(**contact_data)
    created_contact = create_contact(db_session, contact_create)
    retrieved_contact = get_contact(db_session, created_contact.id)
    assert retrieved_contact is not None
    assert retrieved_contact.id == created_contact.id

# Тест для оновлення контакта


def test_update_contact(db_session):
    contact_data = {"name": "John", "surname": "Doe",
                    "email": "john.doe@example.com"}
    contact_create = ContactCreate(**contact_data)
    created_contact = create_contact(db_session, contact_create)
    update_data = {"name": "Updated Name"}
    contact_update = ContactUpdate(**update_data)
    updated_contact = update_contact(
        db_session, created_contact.id, contact_update)
    assert updated_contact is not None
    assert updated_contact.id == created_contact.id
    assert updated_contact.name == update_data["name"]

# Тест для видалення контакта


def test_delete_contact(db_session):
    contact_data = {"name": "John", "surname": "Doe",
                    "email": "john.doe@example.com"}
    contact_create = ContactCreate(**contact_data)
    created_contact = create_contact(db_session, contact_create)
    delete_contact(db_session, created_contact.id)
    retrieved_contact = get_contact(db_session, created_contact.id)
    assert retrieved_contact is None
