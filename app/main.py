from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import List, Optional
from schemas import ContactCreate


# Імпорт бібліотеки bcrypt для хешування паролів
import bcrypt

# Імпорт бібліотеки OAuth2 для аутентифікації з токенами
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from .config import settings  # Імпорт налаштувань

DATABASE_URL = settings.database_url

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Модель контакту


class Contact(Base):
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
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)


# Ініціалізація FastAPI
app = FastAPI()

# Налаштування для аутентифікації та авторизації
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Функція для хешування паролів


def get_password_hash(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Функція для перевірки паролів


def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)

# Функція для створення токена доступу


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Функція для отримання бази даних


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Функція для отримання користувача за електронною поштою


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

# CRUD операції для контактів


@app.post("/contacts/", response_model=Contact)
def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    """
    Створення нового контакту.
    """
    db_contact = Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

# Інші CRUD операції для контактів, які були вам визначені

# Реєстрація користувача


@app.post("/register/", response_model=User)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Реєстрація нового користувача.
    """
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = User(
        **user.dict(), hashed_password=get_password_hash(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Логін користувача та отримання токену


@app.post("/login/", response_model=Token)
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    """
    Логін користувача та отримання JWT токену.
    """
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user is None or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# Отримання даних поточного користувача


@app.get("/users/me/", response_model=User)
def read_user_me(current_user: User = Depends(get_current_user)):
    """
    Отримання даних поточного користувача.
    """
    return current_user

# Функція для отримання поточного користувача з токену


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=400, detail="Could not validate credentials")
    except JWTError:
        raise HTTPException(
            status_code=401, detail="Could not validate credentials")

    db_user = get_user_by_email(db, email)
    if db_user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return db_user

# Оголошення OAuth2PasswordBearer для аутентифікації з токенами
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
