from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from app.models.budget import Budget
from app.models.transaction import Transaction, TransactionType
from app.models.category import Category
from app.schemas.budget import BudgetCreate, BudgetUpdate, BudgetWithProgress
from datetime import datetime

def get_budgets(db: Session, user_id: int, month: int, year: int):
    budgets = db.query(Budget).filter(
        Budget.user_id == user_id,
        Budget.month == month,
        Budget.year == year
    ).all()

    result = []
    for budget in budgets:
        spent = db.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == user_id,
            Transaction.category_id == budget.category_id,
            Transaction.type == TransactionType.expense,
            extract('month', Transaction.date) == month,
            extract('year', Transaction.date) == year
        ).scalar() or 0

        percentage = round((spent / budget.amount) * 100, 1) if budget.amount > 0 else 0

        result.append(BudgetWithProgress(
            id=budget.id,
            amount=budget.amount,
            category_id=budget.category_id,
            category_name=budget.category.name,
            category_color=budget.category.color,
            spent=spent,
            percentage=percentage,
            month=budget.month,
            year=budget.year
        ))

    return result

def create_budget(db: Session, data: BudgetCreate, user_id: int):
    budget = Budget(
        amount=data.amount,
        category_id=data.category_id,
        user_id=user_id,
        month=data.month,
        year=data.year
    )
    db.add(budget)
    db.commit()
    db.refresh(budget)
    return budget

def update_budget(db: Session, budget_id: int, data: BudgetUpdate, user_id: int):
    budget = db.query(Budget).filter(
        Budget.id == budget_id,
        Budget.user_id == user_id
    ).first()
    if not budget:
        return None
    budget.amount = data.amount
    db.commit()
    db.refresh(budget)
    return budget

def delete_budget(db: Session, budget_id: int, user_id: int):
    budget = db.query(Budget).filter(
        Budget.id == budget_id,
        Budget.user_id == user_id
    ).first()
    if not budget:
        return False
    db.delete(budget)
    db.commit()
    return True