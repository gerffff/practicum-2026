from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import User, Book, Favorite
from app.schemas import FavoriteCreate, FavoriteResponse
from app.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=FavoriteResponse)
def add_to_favorites(
    favorite: FavoriteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    book = db.query(Book).filter(Book.id == favorite.book_id).first()
    if not book:
        raise HTTPException(
            status_code=404,
            detail="Книгу не знайдено"
        )
    
    existing_favorite = db.query(Favorite).filter(
        Favorite.user_id == current_user.id,
        Favorite.book_id == favorite.book_id
    ).first()
    
    if existing_favorite:
        raise HTTPException(
            status_code=400,
            detail="Книга вже в улюблених"
        )
    
    db_favorite = Favorite(
        user_id=current_user.id,
        book_id=favorite.book_id
    )
    db.add(db_favorite)
    db.commit()
    db.refresh(db_favorite)
    
    return db_favorite

@router.delete("/{book_id}")
def remove_from_favorites(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    favorite = db.query(Favorite).filter(
        Favorite.user_id == current_user.id,
        Favorite.book_id == book_id
    ).first()
    
    if not favorite:
        raise HTTPException(
            status_code=404,
            detail="Книгу не знайдено в улюблених"
        )
    
    db.delete(favorite)
    db.commit()
    
    return {"message": "Книгу видалено з улюблених"}

@router.get("/", response_model=List[FavoriteResponse])
def get_favorites(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    favorites = db.query(Favorite).filter(Favorite.user_id == current_user.id).all()
    
    favorite_responses = []
    for fav in favorites:
        book = db.query(Book).filter(Book.id == fav.book_id).first()
        if book:
            favorite_response = FavoriteResponse(
                id=fav.id,
                user_id=fav.user_id,
                book_id=fav.book_id,
                created_at=fav.created_at,
                book={
                    "id": book.id,
                    "title": book.title,
                    "description": book.description,
                    "published_year": book.published_year,
                    "created_at": book.created_at
                }
            )
            favorite_responses.append(favorite_response)
    
    return favorite_responses
