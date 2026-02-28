from pydantic import BaseModel
from datetime import datetime

class FavoriteCreate(BaseModel):
    book_id: int

class FavoriteResponse(BaseModel):
    id: int
    user_id: int
    book_id: int
    created_at: datetime
    book: dict
