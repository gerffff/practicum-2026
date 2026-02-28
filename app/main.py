from fastapi import FastAPI

from app.routers.auth import router as auth_router
from app.routers.books import router as books_router
from app.routers.favorites import router as favorites_router
from app.routers.admin import router as admin_router

app = FastAPI(
    title="Онлайн Бібліотека API",
    description="API для онлайн бібліотеки",
    version="1.0.0"
)

app.include_router(auth_router, prefix="/auth", tags=["Авторизація"])
app.include_router(books_router, prefix="/books", tags=["Книги"])
app.include_router(favorites_router, prefix="/favorites", tags=["Обрані книги"])
app.include_router(admin_router, prefix="/admin", tags=["Адміністрування"])

@app.get("/")
def root():
    return {"message": "Онлайн Бібліотека API", "docs": "/docs"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
