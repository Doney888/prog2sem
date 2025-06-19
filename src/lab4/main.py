from database import SessionLocal
from database import init_db
import crud

init_db()

db = SessionLocal()

user = crud.add_user(db, "Alice", "alice@example.com")

book = crud.add_book(db, "SQLAlchemy Guide", "Martin Fowler", 2)

booking = crud.create_booking(db, user.id, book.id)

if booking:
    crud.delete_booking(db, booking.id)

db.close()