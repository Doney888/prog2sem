import unittest
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from models import User, Book, Booking
from crud import add_user, add_book, create_booking, delete_booking


class TestCRUD(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.db = Session()

    def tearDown(self):
        self.db.close()

    def test_add_user(self):
        user = add_user(self.db, "Alice", "alice@example.com")
        self.assertEqual(user.id, 1)
        self.assertEqual(user.name, "Alice")
        self.assertEqual(user.email, "alice@example.com")

        with self.assertRaises(Exception):
            add_user(self.db, "Bob", "alice@example.com")

    def test_add_book(self):
        book = add_book(self.db, "Python Basics", "John Doe", 3)
        self.assertEqual(book.id, 1)
        self.assertEqual(book.title, "Python Basics")
        self.assertEqual(book.author, "John Doe")
        self.assertEqual(book.copies_available, 3)

    def test_create_booking(self):
        user = add_user(self.db, "Alice", "alice@example.com")
        book = add_book(self.db, "Python Basics", "John Doe", 2)

        booking = create_booking(self.db, user.id, book.id)
        self.assertEqual(booking.id, 1)
        self.assertEqual(booking.booking_date, date.today())

        updated_book = self.db.query(Book).get(book.id)
        self.assertEqual(updated_book.copies_available, 1)

        book2 = add_book(self.db, "Out of Stock", "Author", 0)
        booking2 = create_booking(self.db, user.id, book2.id)
        self.assertIsNone(booking2)

    def test_delete_booking(self):
        user = add_user(self.db, "Alice", "alice@example.com")
        book = add_book(self.db, "Python Basics", "John Doe", 1)
        booking = create_booking(self.db, user.id, book.id)

        result = delete_booking(self.db, booking.id)
        self.assertTrue(result)

        updated_book = self.db.query(Book).get(book.id)
        self.assertEqual(updated_book.copies_available, 1)

        # Проверка попытки удаления несуществующего бронирования
        result = delete_booking(self.db, 999)
        self.assertFalse(result)

    def test_relationships(self):
        user = add_user(self.db, "Alice", "alice@example.com")
        book = add_book(self.db, "Python Basics", "John Doe", 2)
        booking = create_booking(self.db, user.id, book.id)

        self.assertEqual(user.bookings[0].id, booking.id)
        self.assertEqual(book.bookings[0].id, booking.id)
        self.assertEqual(booking.user.name, "Alice")
        self.assertEqual(booking.book.title, "Python Basics")


if __name__ == '__main__':
    unittest.main()