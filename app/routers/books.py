from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Book, Author, Genre, BookAuthor, BookGenre
from app.schemas import BookCreate, BookResponse

router = APIRouter()

@router.get("/", response_model=List[BookResponse])
def get_books(db: Session = Depends(get_db)):
    books = db.query(Book).all()
    
    book_responses = []
    for book in books:
        authors = db.query(Author).join(BookAuthor).filter(BookAuthor.book_id == book.id).all()
        
        genres = db.query(Genre).join(BookGenre).filter(BookGenre.book_id == book.id).all()
        
        book_response = BookResponse(
            id=book.id,
            title=book.title,
            description=book.description,
            published_year=book.published_year,
            created_at=book.created_at,
            authors=[{"id": a.id, "name": a.name} for a in authors],
            genres=[{"id": g.id, "name": g.name} for g in genres]
        )
        book_responses.append(book_response)
    
    return book_responses

@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(
            status_code=404,
            detail="Книгу не знайдено"
        )
    
    authors = db.query(Author).join(BookAuthor).filter(BookAuthor.book_id == book.id).all()
    
    genres = db.query(Genre).join(BookGenre).filter(BookGenre.book_id == book.id).all()
    
    return BookResponse(
        id=book.id,
        title=book.title,
        description=book.description,
        published_year=book.published_year,
        created_at=book.created_at,
        authors=[{"id": a.id, "name": a.name} for a in authors],
        genres=[{"id": g.id, "name": g.name} for g in genres]
    )
