from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# User schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    is_admin: bool
    created_at: datetime

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Book schemas
class AuthorResponse(BaseModel):
    id: int
    name: str

class GenreResponse(BaseModel):
    id: int
    name: str

class BookCreate(BaseModel):
    title: str
    description: Optional[str] = None
    published_year: Optional[int] = None
    author_ids: List[int] = []
    genre_ids: List[int] = []

class BookResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    published_year: Optional[int] = None
    created_at: datetime
    authors: List[dict] = []
    genres: List[dict] = []

# Favorite schemas
class FavoriteCreate(BaseModel):
    book_id: int

class FavoriteResponse(BaseModel):
    id: int
    user_id: int
    book_id: int
    created_at: datetime
    book: dict

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
