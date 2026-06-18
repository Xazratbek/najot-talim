from fastapi import APIRouter, Depends
from db import get_db
import book.crud as crud
import book.schema as schema
from sqlalchemy.orm import Session


router = APIRouter()


@router.post('/create-author')
def create_author_router(data:schema.CreateAuthorSchema , session: Session = Depends(get_db)):
    return crud.create_author(session, data)

@router.get('/detail-author/{author_id}')
def detail_author_router(author_id:int, session: Session = Depends(get_db)):
    return crud.author_detail(session, author_id)

@router.get('/list-author/')
def list_author_router(session: Session = Depends(get_db)):
    return crud.author_list(session)

@router.patch('/update-author/{author_id}')
def update_author_router(author_id:int, data: schema.UpdateAuthorSchema ,session: Session = Depends(get_db)):
    return crud.update_author(session, data, author_id)

@router.delete('/delete-author/{author_id}')
def delete_author_router(author_id:int, session: Session = Depends(get_db)):
    return crud.author_delete(session, author_id)


#CATEGORY
@router.post('/create-category')
def create_category_router(data:schema.CreateCategorySchema , session: Session = Depends(get_db)):
    return crud.create_category(session, data)

@router.get('/detail-category/{category_id}')
def detail_category_router(category_id:int, session: Session = Depends(get_db)):
    return crud.category_detail(session, category_id)

@router.get('/list-category/')
def list_category_router(session: Session = Depends(get_db)):
    return crud.category_list(session)

@router.patch('/update-category/{category_id}')
def update_category_router(category_id:int, data: schema.UpdateCategorySchema ,session: Session = Depends(get_db)):
    return crud.update_category(session, data, category_id)

@router.delete('/delete-category/{category_id}')
def delete_category_router(category_id:int, session: Session = Depends(get_db)):
    return crud.category_delete(session, category_id)

#BOOK
@router.post('/create-book')
def create_book_router(data:schema.CreateBookSchema , session: Session = Depends(get_db)):
    return crud.create_book(session, data)

@router.get('/detail-book/{book_id}')
def detail_book_router(book_id:int, session: Session = Depends(get_db)):
    return crud.book_detail(session, book_id)

@router.get('/list-book/')
def list_book_router(session: Session = Depends(get_db)):
    return crud.book_list(session)

@router.patch('/update-book/{book_id}')
def update_book_router(book_id:int, data: schema.UpdateBookSchema ,session: Session = Depends(get_db)):
    return crud.update_book(session, data, book_id)

@router.delete('/delete-book/{book_id}')
def delete_book_router(book_id:int, session: Session = Depends(get_db)):
    return crud.book_delete(session, book_id)

@router.post('/comment/create')
def create_comment_author(data: schema.CreateCommentSchema,session: Session = Depends(get_db)):
    return crud.create_comment(session=session,data=data)

@router.patch('/comment/update')
def update_comment_schem(data: schema.UpdateCommentSchema,comment_id: int, session: Session = Depends(get_db)):
    return crud.update_comment(session,data,comment_id)

@router.get('/book/comments/{book_id}')
def get_book_comments_list(book_id: int, session: Session = Depends(get_db)):
    return crud.book_comments_list(session,book_id)

@router.delete('/saved/book/delete/{book_id}')
def delete_book_router(book_id: int, user: str, session: Session = Depends(get_db)):
    return crud.delete_saved(session,book_id,user)

@router.post('/save/{book_id}')
def save_book(data: schema.CreateSavedSchema, session: Session = Depends(get_db)):
    return crud.create_saved(session,data)

@router.get('/saved/book/{user}', response_model=schema.SavedUserBooksResponse)
def get_user_saved_books_router(user: str, session: Session = Depends(get_db)):
    return crud.get_user_saved_books(session,user)

@router.delete('comment/{comment_id}')
def delete_comment_router(comment_id: int, session: Session = Depends(get_db)):
    return crud.delete_comment(session,comment_id)