from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class WishlistCreate(BaseModel):
    book_id: UUID


class WishlistResponse(BaseModel):
    id: UUID
    book_id: UUID
    user_id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True