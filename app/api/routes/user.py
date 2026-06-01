from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.db.database import Base, get_db
from app.models.user import User

router = APIRouter()


@router.get("/")
def get_users(db: Session = Depends(get_db)):
    dbData = db.query(User).all()
    return {"users": dbData}
    return {"message": "List of users", "users": ["sakib", "john", "doe"]}


@router.post("/")
def create_user(payload: UserCreate, db: Session = Depends(get_db)):

    dbData = db.query(User).all()
    return {"users": dbData}
    new_user = User(email=payload.email, username=payload.username)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
