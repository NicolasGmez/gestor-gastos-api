from pydantic import BaseModel
from datetime import datetime

class SavingsGoalCreate(BaseModel):
    name: str
    target_amount: float
    icon: str = "target"

class SavingsGoalResponse(BaseModel):
    id: int
    name: str
    target_amount: float
    icon: str
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class SavingsGoalWithProgress(BaseModel):
    id: int
    name: str
    target_amount: float
    icon: str
    current_amount: float
    percentage: float
    remaining: float