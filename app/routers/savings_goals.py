from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.savings_goal import SavingsGoalCreate, SavingsGoalResponse, SavingsGoalWithProgress
from app.services.savings_goal_service import get_goals, create_goal, delete_goal

router = APIRouter(prefix="/savings-goals", tags=["Savings Goals"])

@router.get("/", response_model=list[SavingsGoalWithProgress])
def list_goals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_goals(db, current_user.id)

@router.post("/", response_model=SavingsGoalResponse, status_code=201)
def create_new_goal(
    data: SavingsGoalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_goal(db, data, current_user.id)

@router.delete("/{goal_id}", status_code=204)
def delete_existing_goal(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deleted = delete_goal(db, goal_id, current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Meta no encontrada")