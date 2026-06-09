from fastapi import FastAPI
from app.api.routes.user import router as user_router
from app.api.routes.shelves import router as shelves_router
from app.api.routes.books import router as books_router
from app.api.routes.user_book import router as user_books_router
from app.api.routes.auth import router as auth_router
from app.api.routes.note import router as note_router
from app.api.routes.highlights import router as highlights_router
from app.api.routes.wishlist import router as wishlist_router
from app.api.routes.reading_goals import router as reading_goals_router
from app.api.routes.dashboard import router as dashboard_router
from app.api.routes.activity import router as activity_router
from app.api.routes.admin import router as admin_router
from app.api.routes import authors
import app.models

app = FastAPI()
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(shelves_router, prefix="/shelves", tags=["Shelves"])
app.include_router(books_router, prefix="/books", tags=["Books"])
app.include_router(user_books_router, prefix="/user-books", tags=["User Books"])
app.include_router(note_router, prefix="/notes", tags=["User Notes"])
app.include_router(highlights_router, prefix="/highlights", tags=["Highlights"])
app.include_router(wishlist_router, prefix="/wishlist", tags=["wishlist"])
app.include_router(
    reading_goals_router, prefix="/reading-goals", tags=["Reading Goals"]
)
app.include_router(dashboard_router, prefix="/dashboard", tags=["User Dashboard"])
app.include_router(activity_router, prefix="/activities", tags=["User activities"])
app.include_router(admin_router, prefix="/admin", tags=["Admin"])
app.include_router(
    authors.router,
    prefix="/authors",
    tags=["Authors"],
)

@app.get("/")
def roots():
    return {"message": "IlmShelf Backend Running"}
