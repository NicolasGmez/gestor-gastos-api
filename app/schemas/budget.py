from pydantic import BaseModel
from datetime import datetime

class BudgetCreate(BaseModel):
    amount: float
    category_id: int
    month: int
    year: int

class BudgetUpdate(BaseModel):
    amount: float

class BudgetResponse(BaseModel):
    id: int
    amount: float
    category_id: int
    user_id: int
    month: int
    year: int
    created_at: datetime

    class Config:
        from_attributes = True

class BudgetWithProgress(BaseModel):
    id: int
    amount: float
    category_id: int
    category_name: str
    category_color: str
    spent: float
    percentage: float
    month: int
    year: int