from sqlalchemy.orm import Session
from . import models
from schemas import ContactCreate


def create_contact(db: Session, contact: models.Contact):
    """
    Створює новий контакт.

    Args:
        db (Session): Об'єкт сесії бази даних.
        contact (Contact): Об'єкт контакту, який буде створено.

    Returns:
        Contact: Створений контакт.

    """
    db_contact = models.Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def get_contacts(db: Session, skip: int = 0, limit: int = 100):
    """
    Отримує список контактів з можливістю пагінації.

    Args:
        db (Session): Об'єкт сесії бази даних.
        skip (int, optional): Кількість записів для пропуску (пагінація). За замовчуванням 0.
        limit (int, optional): Максимальна кількість записів для отримання (пагінація). За замовчуванням 100.

    Returns:
        List[Contact]: Список контактів.

    """
    return db.query(models.Contact).offset(skip).limit(limit).all()


def get_contact(db: Session, contact_id: int):
    """
    Отримує контакт за ідентифікатором.

    Args:
        db (Session): Об'єкт сесії бази даних.
        contact_id (int): Ідентифікатор контакту.

    Returns:
        Contact: Знайдений контакт.

    """
    return db.query(models.Contact).filter(models.Contact.id == contact_id).first()


def update_contact(db: Session, contact_id: int, updated_contact: models.Contact):
    """
    Оновлює існуючий контакт за ідентифікатором.

    Args:
        db (Session): Об'єкт сесії бази даних.
        contact_id (int): Ідентифікатор контакту, який потрібно оновити.
        updated_contact (Contact): Об'єкт контакту з оновленими даними.

    Returns:
        Contact: Оновлений контакт.

    """
    db_contact = db.query(models.Contact).filter(
        models.Contact.id == contact_id).first()
    if db_contact:
        for attr, value in updated_contact.dict().items():
            setattr(db_contact, attr, value)
        db.commit()
        db.refresh(db_contact)
        return db_contact
    return None


def delete_contact(db: Session, contact_id: int):
    """
    Видаляє контакт за ідентифікатором.

    Args:
        db (Session): Об'єкт сесії бази даних.
        contact_id (int): Ідентифікатор контакту, який потрібно видалити.

    Returns:
        bool: True, якщо контакт успішно видалено; інакше False.

    """
    db_contact = db.query(models.Contact).filter(
        models.Contact.id == contact_id).first()
    if db_contact:
        db.delete(db_contact)
        db.commit()
        return True
    return False
