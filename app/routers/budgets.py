from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.budget import BudgetCreate, BudgetUpdate, BudgetResponse, BudgetWithProgress
from app.services.budget_service import get_budgets, create_budget, update_budget, delete_budget

router = APIRouter(prefix="/budgets", tags=["Budgets"])

@router.get("/", response_model=list[BudgetWithProgress])
def list_budgets(
    month: int = None,
    year: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    now = datetime.now()
    m = month or now.month
    y = year or now.year
    return get_budgets(db, current_user.id, m, y)

@router.post("/", response_model=BudgetResponse, status_code=201)
def create_new_budget(
    data: BudgetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return create_budget(db, data, current_user.id)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Ya existe un presupuesto para esta categoría en este mes"
        )

@router.put("/{budget_id}", response_model=BudgetResponse)
def update_existing_budget(
    budget_id: int,
    data: BudgetUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    budget = update_budget(db, budget_id, data, current_user.id)
    if not budget:
        raise HTTPException(status_code=404, detail="Presupuesto no encontrado")
    return budget

@router.delete("/{budget_id}", status_code=204)
def delete_existing_budget(
    budget_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deleted = delete_budget(db, budget_id, current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Presupuesto no encontrado")