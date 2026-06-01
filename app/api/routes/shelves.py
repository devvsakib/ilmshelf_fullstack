from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.shelf import Shelf
from pydantic import BaseModel
from app.models.enums import ShelfTypeEnum
from app.schemas.shelf import ShelfCreate
import uuid

router = APIRouter()


@router.get("/")
def get_shelves(db: Session = Depends(get_db)):
    shelves = db.query(Shelf).all()
    return {
        "message": "List of shelves",
        "shelves": shelves,
    }


@router.post("/")
def create_shelve(payload: ShelfCreate, db: Session = Depends(get_db)):
    existing = db.query(Shelf).filter(Shelf.slug == payload.slug).first()

    if existing:
        return "Shelve with this slug already exists!"

    shelf = Shelf(
        name=payload.name,
        slug=payload.slug,
        type=payload.type,
        is_public=payload.is_public,
        created_by=payload.created_by,
    )

    db.add(shelf)
    db.commit()
    db.refresh(shelf)

    return {"message": "Shelf created", "shelf": shelf}
