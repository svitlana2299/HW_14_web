from . import models, crud, auth
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from schemas import ContactCreate

# Імпорт моделей з models.py
from .models import User, Hashing

# Оголошення OAuth2PasswordBearer для аутентифікації з токенами
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Ініціалізація FastAPI

DATABASE_URL = "postgresql://username:password@localhost/dbname"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()

# Налаштування для аутентифікації та авторизації
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Функція для хешування паролів


def get_password_hash(password):
    return Hashing.get_password_hash(password)

# Функція для перевірки паролів


def verify_password(plain_password, hashed_password):
    return Hashing.verify_password(plain_password, hashed_password)

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

# Реєстрація користувача


@app.post("/register/", response_model=User)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Реєстрація нового користувача.

    Args:
        user (UserCreate): Дані для створення користувача.

    Returns:
        User: Зареєстрований користувач.

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

    Args:
        user (UserLogin): Дані для авторизації.

    Returns:
        Token: JWT токен доступу.

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

    Args:
        current_user (User): Поточний користувач (отриманий з токену).

    Returns:
        User: Дані поточного користувача.

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

    db_user = crud.get_user_by_email(db, email)
    if db_user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return db_user
