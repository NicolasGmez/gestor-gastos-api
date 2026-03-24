from sqlalchemy import func
from app.models.transaction import TransactionType
from app.models.category import Category
from app.models.transaction import Transaction
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.transaction import TransactionCreate, TransactionUpdate, TransactionResponse
from app.services.transaction_service import (
    get_transactions, get_transaction, create_transaction,
    update_transaction, delete_transaction
)

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.get("/", response_model=list[TransactionResponse])
def list_transactions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_transactions(db, current_user.id)

@router.post("/", response_model=TransactionResponse, status_code=201)
def create_new_transaction(
    data: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_transaction(db, data, current_user.id)

@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_one_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    transaction = get_transaction(db, transaction_id, current_user.id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    return transaction

@router.put("/{transaction_id}", response_model=TransactionResponse)
def update_existing_transaction(
    transaction_id: int,
    data: TransactionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    transaction = update_transaction(db, transaction_id, data, current_user.id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    return transaction

@router.delete("/{transaction_id}", status_code=204)
def delete_existing_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deleted = delete_transaction(db, transaction_id, current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    
@router.get("/stats/summary")
def get_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    total_income = db.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == current_user.id,
        Transaction.type == TransactionType.income
    ).scalar() or 0

    total_expenses = db.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == current_user.id,
        Transaction.type == TransactionType.expense
    ).scalar() or 0

    by_category = db.query(
        Category.name,
        Category.color,
        func.sum(Transaction.amount).label("total")
    ).join(Transaction, Transaction.category_id == Category.id).filter(
        Transaction.user_id == current_user.id,
        Transaction.type == TransactionType.expense
    ).group_by(Category.name, Category.color).all()

    return {
        "total_income": round(total_income, 2),
        "total_expenses": round(total_expenses, 2),
        "balance": round(total_income - total_expenses, 2),
        "by_category": [
            {"name": r.name, "color": r.color, "total": round(r.total, 2)}
            for r in by_category
        ]
    }    
