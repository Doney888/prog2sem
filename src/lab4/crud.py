from sqlalchemy.orm import Session
import models
from datetime import date


def add_user(db: Session, name: str, email: str):
    """
    Функция для добавления пользователя
    :param db: таблица, куда мы добавляем пользователя
    :param name: имя пользователя
    :param email: почта пользователя
    :return: возвращает объект пользователя
    """
    user = models.User(name=name, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def add_book(db: Session, title: str, author: str, copies: int):
    """
    Функция для добавления книги
    :param db: таблица, куда мы добавляем книгу
    :param title: название книги
    :param author: автор книги
    :param copies: количество копий
    :return: объект книги
    """
    book = models.Book(title=title, author=author, copies_available=copies)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def create_booking(db: Session, user_id: int, book_id: int):
    """
    Функция для бронирования книги
    :param db: таблица с бронью
    :param user_id: id пользователя, который бронирует книгу
    :param book_id: id книги
    :return: объект брони, если забронировать книгу удалось, иначе none
    """
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book or book.copies_available < 1:
        return None

    booking = models.Booking(
        user_id=user_id,
        book_id=book_id,
        booking_date=date.today()
    )

    book.copies_available -= 1

    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


def delete_booking(db: Session, booking_id: int):
    """
    Функция для удаления брони
    :param db: таблица, из которой удаляем бронь
    :param booking_id: id брони
    :return: True, если удаление удалось, иначе False
    """
    booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if booking:
        book = db.query(models.Book).get(booking.book_id)
        book.copies_available += 1

        db.delete(booking)
        db.commit()
        return True
    return False