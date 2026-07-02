from book.models import *
from book.schema import *
from sqlalchemy.orm import Session, joinedload
from db import SessionLocal
from fastapi.exceptions import HTTPException
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from auth.models import User


def get_object(session, id, model):
    obj = session.query(model).filter(model.id == id).first()
    if not obj:
        raise HTTPException(
            detail={
                'message': f"{model} not found",
            },
            status_code=status.HTTP_404_NOT_FOUND
        )
    return obj


def check_owner_or_admin(user: User, owner_username: str):
    if user.username != owner_username and not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bu amalni faqat egasi yoki admin bajara oladi"
        )


def response_model(msg, status, data, etc = None):
    return {
        'msg': msg,
        'status': status,
        'etc': etc,
        'data': data,
    } if etc else {
        'msg': msg,
        'status': status,
        'data': data,
    }


#AUTHOR

def create_author(session: Session, data: CreateAuthorSchema):
    author = Author(name=data.name, year=data.year)
    session.add(author)
    session.commit()
    session.refresh(author)

    return response_model('Author created', status.HTTP_201_CREATED, author)


def update_author(session: Session, data: UpdateAuthorSchema, author_id: int):
    author = get_object(session, author_id, Author)

    data = data.model_dump(exclude_unset=True)

    for key, value in data.items():
        setattr(author, key, value)

    session.commit()
    session.refresh(author)

    return response_model('Author updated', status.HTTP_200_OK, author)


def author_detail(session: Session, author_id: int):
    author = get_object(session, author_id, Author)
    return response_model('Author', status.HTTP_200_OK, {'author': {author}, 'books': author.books})


def author_list(session: Session, search: str = None):
    query = session.query(Author)

    if search:
        query = query.filter(Author.name.ilike(f'%{search}%'))

    authors = query.order_by(Author.id.desc()).all()
    return response_model('Author', status.HTTP_200_OK, authors)

def author_delete(session: Session, author_id: int):
    author = get_object(session, author_id, Author)
    session.delete(author)
    session.commit()
    return response_model('Author deleted', status.HTTP_204_NO_CONTENT, data=None)



#CATEGORY
def create_category(session: Session, data: CreateCategorySchema):
    category = Category(title=data.title)
    session.add(category)
    session.commit()
    session.refresh(category)

    return response_model('Category created', status.HTTP_201_CREATED, category)

def update_category(session: Session, data: UpdateCategorySchema, category_id: int):
    category = get_object(session, category_id, Category)

    data = data.model_dump(exclude_unset=True)

    for key, value in data.items():
        setattr(category, key, value)

    session.commit()
    session.refresh(category)

    return response_model('Category updated', status.HTTP_200_OK, category)


def category_detail(session: Session, category_id: int):
    category = get_object(session, category_id, Category)
    return response_model('category', status.HTTP_200_OK, {'category': {category}, 'books': category.books})

def category_delete(session: Session, category_id:int):
    category = get_object(session, category_id, Category)
    session.delete(category)
    session.commit()
    return response_model('category deleted', status.HTTP_204_NO_CONTENT, data=None)


def category_list(session: Session, search: str = None):
    query = session.query(Category)

    if search:
        query = query.filter(Category.title.ilike(f'%{search}%'))

    categories = query.order_by(Category.id.desc()).all()
    return response_model('category', status.HTTP_200_OK, categories)


#BOOK

def create_book(session: Session, data: CreateBookSchema):
    book = Book(**data.model_dump())
    session.add(book)
    session.commit()
    session.refresh(book)

    return response_model('book created', status.HTTP_201_CREATED, book)

def update_book(session: Session, data: UpdateBookSchema, book_id: int):
    book = get_object(session, book_id, Book)

    data = data.model_dump(exclude_unset=True)

    for key, value in data.items():
        setattr(book, key, value)

    session.commit()
    session.refresh(book)

    return response_model('book updated', status.HTTP_200_OK, book)


def book_detail(session: Session, book_id: int):

    book = (
        session.query(Book)
        .options(
            joinedload(Book.author),
            joinedload(Book.category),
            joinedload(Book.comments)
        )
        .filter(Book.id == book_id)
        .first()
    )

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Book not found'
        )

    return {
        'id': book.id,
        'title': book.title,
        'year': book.year,
        'price': float(book.price),
        'desc': book.desc,
        'is_published': book.is_published,
        'created_at': book.created_at,

        'author': {
            'id': book.author.id,
            'name': book.author.name,
            'year': book.author.year,
        },

        'category': {
            'id': book.category.id,
            'title': book.category.title,
        },

        'comments':  book.comments

    }

def book_delete(session: Session, book_id:int):
    book = get_object(session, book_id, Book)
    session.delete(book)
    session.commit()
    return response_model('book deleted', status.HTTP_204_NO_CONTENT, data=None)


def book_list(
    session: Session,
    search: str = None,
    author_id: int = None,
    category_id: int = None,
    is_published: bool = None,
):
    query = session.query(Book).options(joinedload(Book.author))

    if search:
        query = query.filter(Book.title.ilike(f'%{search}%'))

    if author_id:
        query = query.filter(Book.author_id == author_id)

    if category_id:
        query = query.filter(Book.category_id == category_id)

    if is_published is not None:
        query = query.filter(Book.is_published == is_published)

    books = query.order_by(Book.id.desc()).all()
    return response_model('book', status.HTTP_200_OK, books)


def create_comment(session: Session, data: CreateCommentSchema, user: User):
    comment = Comment(summary=data.summary, book_id=data.book_id, user=user.username)
    session.add(comment)
    session.commit()
    session.refresh(comment)

    response = {
        'msg': 'comment created',
        'status': status.HTTP_201_CREATED,
        'comment': comment
    }

    return response

def delete_comment(session: Session, comment_id: int, user: User):
    comment = get_object(session, comment_id, Comment)
    check_owner_or_admin(user, comment.user)

    session.delete(comment)
    session.commit()
    return response_model('Comment deleted', status.HTTP_204_NO_CONTENT, data=None)

def update_comment(session: Session, data: UpdateCommentSchema, comment_id: int, user: User):
    comment = get_object(session, comment_id, Comment)
    check_owner_or_admin(user, comment.user)

    data = data.model_dump(exclude_unset=True)

    for key, value in data.items():
        setattr(comment, key, value)

    session.commit()
    session.refresh(comment)

    return {
        "message": f"comment: {comment_id}-id dagi comment yangilandi",
        "status": status.HTTP_200_OK
    }

def book_comments_list(session: Session, book_id: int):
    comments = session.query(Comment).filter(Comment.book_id == book_id).all()

    return {"message": "Barcha commentlar","comments": comments}

def create_saved(session: Session, book_id: int, user: User):
    saved = Saved(book_id=book_id, user=user.username)
    session.add(saved)
    session.commit()
    session.refresh(saved)

    response = {
        'msg': 'saved created',
        'status': status.HTTP_201_CREATED,
        'saved': saved
    }

    return response

def get_user_saved_books(session: Session, user: User):
    saved = session.query(Saved).filter(Saved.user == user.username).options(
        joinedload(Saved.book).joinedload(Book.author),
        joinedload(Saved.book).joinedload(Book.category)
    ).all()

    if not saved:
        return {"user": user.username, "books": []}

    return {
        "user": user.username,
        "books": [s.book for s in saved]
    }

def delete_saved(session: Session, book_id: int, user: User):
    saved = session.query(Saved).filter(Saved.book_id == book_id, Saved.user == user.username).first()
    if saved:
        session.delete(saved)
        session.commit()
        return {"ok": True, "saved": saved}
    else:
        return {"message": "Saqlanganlar orasida ushbu kitob mavjud emas"}
