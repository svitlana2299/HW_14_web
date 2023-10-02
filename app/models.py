from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from passlib.context import CryptContext
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

# Модель контакту


class Contact(Base):
    """
    Модель для зберігання контактів.

    Attributes:
        id (int): Унікальний ідентифікатор контакту.
        first_name (str): Ім'я контакту.
        last_name (str): Прізвище контакту.
        email (str): Електронна адреса контакту (унікальна).
        phone_number (str): Номер телефону контакту.
        birth_date (datetime): День народження контакту.
        additional_data (str, optional): Додаткові дані про контакт (необов'язково).

    """

    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String, index=True)
    birth_date = Column(DateTime)
    additional_data = Column(String, nullable=True)

# Модель користувача


class User(Base):
    """
    Модель для зберігання користувачів.

    Attributes:
        id (int): Унікальний ідентифікатор користувача.
        username (str): Ім'я користувача (унікальне).
        email (str): Електронна адреса користувача (унікальна).
        hashed_password (str): Захешований пароль користувача.
        is_active (bool): Прапорець активності користувача.
        created_at (datetime): Дата створення користувача (автоматично встановлюється).
        updated_at (datetime): Дата останнього оновлення користувача (автоматично оновлюється).

    """

    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

# Клас для хешування паролів


class Hashing:
    """
    Клас для хешування паролів користувачів.

    Attributes:
        pwd_context (CryptContext): Об'єкт для генерації та перевірки хешів паролів.

    """

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def verify_password(cls, plain_password, hashed_password):
        """
        Перевіряє, чи відповідає звичайний пароль хешу пароля.

        Args:
            plain_password (str): Звичайний пароль.
            hashed_password (str): Захешований пароль.

        Returns:
            bool: True, якщо пароль співпадає з хешем, інакше False.

        """
        return cls.pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def get_password_hash(cls, password):
        """
        Генерує хеш пароля.

        Args:
            password (str): Звичайний пароль.

        Returns:
            str: Захешований пароль.

        """
        return cls.pwd_context.hash(password)
