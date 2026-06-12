from models import Book


def create_book(db, book):
    new_book = Book(
        **book.dict()
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


def list_books(db):
    return db.query(Book).all()


def read_book(db, book_id):
    return db.query(Book).filter(Book.id == book_id).first()


def update_book(db, book_id, book):
    existing = read_book(db, book_id)
    if not existing:
        return None
    existing.title = book.title
    existing.author = book.author
    db.commit()
    db.refresh(existing)
    return existing


def patch_book(db, book_id, book_data):
    existing = read_book(db, book_id)
    if not existing:
        return None
    if book_data.title is not None:
        existing.title = book_data.title
    if book_data.author is not None:
        existing.author = book_data.author
    db.commit()
    db.refresh(existing)
    return existing