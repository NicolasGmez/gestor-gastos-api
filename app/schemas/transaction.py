from pydantic import BaseModel
from datetime import datetime
from app.models.transaction import TransactionType

class TransactionCreate(BaseModel):
    amount: float
    description: str
    type: TransactionType
    category_id: int | None = None
    date: datetime | None = None

class TransactionUpdate(BaseModel):
    amount: float | None = None
    description: str | None = None
    type: TransactionType | None = None
    category_id: int | None = None
    date: datetime | None = None

class TransactionResponse(BaseModel):
    id: int
    amount: float
    description: str
    type: TransactionType
    category_id: int | None
    user_id: int
    date: datetime

    class Config:
        from_attributes = True