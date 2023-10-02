from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

# Модель контакту для валідації даних


class ContactBase(BaseModel):
    first_name: str = Field(..., title="Ім'я контакту", max_length=50)
    last_name: str = Field(..., title="Прізвище контакту", max_length=50)
    email: EmailStr = Field(..., title="Електронна адреса контакту")
    phone_number: str = Field(...,
                              title="Номер телефону контакту", max_length=20)
    birth_date: datetime = Field(..., title="Дата народження контакту",
                                 description="Формат: YYYY-MM-DD")
    additional_data: Optional[str] = Field(
        None, title="Додаткові дані про контакт", max_length=250)

# Модель контакту для створення


class ContactCreate(ContactBase):
    pass

# Модель контакту для оновлення


class ContactUpdate(ContactBase):
    pass

# Модель користувача для реєстрації


class UserCreate(BaseModel):
    username: str = Field(..., title="Ім'я користувача", max_length=50)
    email: EmailStr = Field(..., title="Електронна адреса користувача")
    password: str = Field(..., title="Пароль користувача",
                          min_length=8, max_length=50)

# Модель користувача для логіну


class UserLogin(BaseModel):
    email: EmailStr = Field(..., title="Електронна адреса користувача")
    password: str = Field(..., title="Пароль користувача",
                          min_length=8, max_length=50)

# Модель токена


class Token(BaseModel):
    access_token: str = Field(..., title="Токен доступу",
                              description="JWT токен для авторизації")
    token_type: str = Field("bearer", title="Тип токена",
                            description="Тип токена (зазвичай bearer)")

# Модель поточного користувача


class User(BaseModel):
    username: str = Field(..., title="Ім'я користувача", max_length=50)
    email: EmailStr = Field(..., title="Електронна адреса користувача")
    is_active: bool = Field(..., title="Активність користувача")

    class Config:
        orm_mode = True
