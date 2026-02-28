from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import csv
from io import StringIO

from app.database import get_db
from app.models import User, Book, Author, Genre, BookAuthor, BookGenre
from app.schemas import BookCreate, BookResponse
from app.auth import get_current_user

router = APIRouter()

@router.post("/books", response_model=BookResponse)
def create_book(
    book: BookCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Доступ заборонено"
        )
    
    db_book = Book(
        title=book.title,
        description=book.description,
        published_year=book.published_year
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    
    for author_id in book.author_ids:
        author = db.query(Author).filter(Author.id == author_id).first()
        if author:
            book_author = BookAuthor(book_id=db_book.id, author_id=author.id)
            db.add(book_author)
    
    for genre_id in book.genre_ids:
        genre = db.query(Genre).filter(Genre.id == genre_id).first()
        if genre:
            book_genre = BookGenre(book_id=db_book.id, genre_id=genre.id)
            db.add(book_genre)
    
    db.commit()
    
    return BookResponse(
        id=db_book.id,
        title=db_book.title,
        description=db_book.description,
        published_year=db_book.published_year,
        created_at=db_book.created_at,
        authors=[{"id": a.id, "name": a.name} for a in db.query(Author).join(BookAuthor).filter(BookAuthor.book_id == db_book.id).all()],
        genres=[{"id": g.id, "name": g.name} for g in db.query(Genre).join(BookGenre).filter(BookGenre.book_id == db_book.id).all()]
    )

@router.delete("/books/{book_id}")
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Доступ заборонено"
        )
    
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(
            status_code=404,
            detail="Книгу не знайдено"
        )
    
    db.query(BookAuthor).filter(BookAuthor.book_id == book_id).delete()
    db.query(BookGenre).filter(BookGenre.book_id == book_id).delete()
    
    db.delete(book)
    db.commit()
    
    return {"message": "Книгу видалено"}

@router.get("/export/csv")
def export_books_csv(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Доступ заборонено"
        )
    
    books = db.query(Book).all()
    
    output = StringIO()
    writer = csv.writer(output)
    
    writer.writerow(["ID", "Назва", "Опис", "Рік видання", "Дата створення"])
    
    for book in books:
        writer.writerow([
            book.id,
            book.title,
            book.description or "",
            book.published_year or "",
            book.created_at.strftime("%Y-%m-%d %H:%M:%S")
        ])
    
    output.seek(0)
    return output.getvalue()

@router.put("/users/{user_id}/role")
def change_user_role(
    user_id: int,
    is_admin: bool,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Доступ заборонено"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="Користувача не знайдено"
        )
    
    user.is_admin = is_admin
    db.commit()
    
    return {"message": f"Роль користувача {user.email} змінено"}
