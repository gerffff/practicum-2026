from fastapi import APIRouter
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.book import Book

router = APIRouter(prefix="/test", tags=["test"])

@router.get("/books")
def get_books_simple(db: Session = Depends(get_db)):
    books = db.query(Book).all()
    result = []
    for book in books:
        result.append({
            "id": book.id,
            "title": book.title,
            "description": book.description,
            "published_year": book.published_year,
            "created_at": book.created_at.isoformat() if book.created_at else None
        })
    return result
