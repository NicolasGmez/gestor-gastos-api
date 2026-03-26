from pydantic import BaseModel
from datetime import datetime
from app.models.category import CategoryType

class CategoryCreate(BaseModel):
    name: str
    color: str = "#6366f1"
    type: CategoryType = CategoryType.expense

class CategoryUpdate(BaseModel):
    name: str | None = None
    color: str | None = None
    type: CategoryType | None = None

class CategoryResponse(BaseModel):
    id: int
    name: str
    color: str
    type: CategoryType
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True