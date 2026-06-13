from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.user import UserCreate, UserResponse, UserLogin

from app.services.auth_service import create_user, login_user
from app.core.auth import get_current_user 
from app.models.user import User

router = APIRouter()


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


@router.post("/register", response_model=UserResponse)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    try:
        return create_user(payload=payload, db=db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
def login(payload: UserLogin, db: Session = Depends(get_db)):
    try:
        return login_user(email=payload.email, password=payload.password, db=db)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.get("/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)):
    return current_user
