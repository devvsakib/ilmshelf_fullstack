from uuid import UUID

from pydantic import BaseModel


class BookTagCreate(BaseModel):
    tag_id: UUID