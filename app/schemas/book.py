from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

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
