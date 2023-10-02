import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.config import settings
from app.models import Base
from app.crud import create_contact, get_contact
from app.schemas import ContactCreate


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
    response = client.post("/contacts/", json=contact_data)
    assert response.status_code == 201
    created_contact = response.json()
    assert created_contact["name"] == contact_data["name"]
    assert created_contact["surname"] == contact_data["surname"]
    assert created_contact["email"] == contact_data["email"]
    db_contact = get_contact(db_session, created_contact["id"])
    assert db_contact is not None
    assert db_contact.name == contact_data["name"]
    assert db_contact.surname == contact_data["surname"]
    assert db_contact.email == contact_data["email"]

# Тест для отримання списку контактів


def test_read_contacts(db_session):
    response = client.get("/contacts/")
    assert response.status_code == 200
    contacts = response.json()
    assert len(contacts) > 0
