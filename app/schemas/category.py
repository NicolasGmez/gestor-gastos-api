from pydantic import BaseModel
from datetime import datetime

class CategoryCreate(BaseModel):
    name: str
    color: str = "#6366f1"

class CategoryUpdate(BaseModel):
    name: str | None = None
    color: str | None = None

class CategoryResponse(BaseModel):
    id: int
    name: str
    color: str
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True