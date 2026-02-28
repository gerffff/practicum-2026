from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    published_year = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Связи
    authors = relationship("BookAuthor", back_populates="book")
    genres = relationship("BookGenre", back_populates="book")
    favorites = relationship("Favorite", back_populates="book")

class BookAuthor(Base):
    __tablename__ = "book_authors"

    book_id = Column(Integer, ForeignKey("books.id"), primary_key=True)
    author_id = Column(Integer, ForeignKey("authors.id"), primary_key=True)
    
    # Связи
    book = relationship("Book", back_populates="authors")
    author = relationship("Author", back_populates="books")

class BookGenre(Base):
    __tablename__ = "book_genres"

    book_id = Column(Integer, ForeignKey("books.id"), primary_key=True)
    genre_id = Column(Integer, ForeignKey("genres.id"), primary_key=True)
    
    # Связи
    book = relationship("Book", back_populates="genres")
    genre = relationship("Genre", back_populates="books")
