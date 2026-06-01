from fastapi import FastAPI
from app.api.routes.user import router as user_router
from app.api.routes.shelves import router as shelves_router
from app.api.routes.books import router as books_router
from app.api.routes.userBooks import router as user_books_router
from app.api.routes.auth import router as auth_router

import app.models

app = FastAPI()
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(shelves_router, prefix="/shelves", tags=["Shelves"])
app.include_router(books_router, prefix="/books", tags=["Books"])
app.include_router(user_books_router, prefix="/user-books", tags=["User Books"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])


@app.get("/")
def roots():
    return {"message": "IlmShelf Backend Running"}
