from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.user import UserCreate, UserResponse, UserLogin

from app.services.auth_service import create_user, login_user
from app.core.dependencies import get_current_user 
from app.models.user import User

router = APIRouter()

@router.get("/users")
def get_users():
    pass
@router.get("/users/{id}")
def get_user():
    pass

@router.delete("/users/{id}")
def delete_users():
    pass

@router.patch("/users/{id}/promote")
def promote_users():
    pass

@router.patch("/users/{id}/demote")
def demote_users():
    pass


# Books
@router.get("/books")
def get_books():
    pass

@router.delete("/books/{id}")
def delete_book():
    pass

# Shelves
@router.get("/shelves")
def get_shelves():
    pass

@router.delete("/shelves/{id}")
def delete_shelve():
    pass

# dashboard
@router.get("/dashboard")
def dashboard():
    pass