from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.savings_goal import SavingsGoal
from app.models.transaction import Transaction, TransactionType
from app.schemas.savings_goal import SavingsGoalCreate, SavingsGoalWithProgress

def get_balance(db: Session, user_id: int) -> float:
    income = db.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == user_id,
        Transaction.type == TransactionType.income
    ).scalar() or 0

    expenses = db.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == user_id,
        Transaction.type == TransactionType.expense
    ).scalar() or 0

    return income - expenses

def get_goals(db: Session, user_id: int):
    goals = db.query(SavingsGoal).filter(
        SavingsGoal.user_id == user_id
    ).all()

    balance = get_balance(db, user_id)
    result = []

    for goal in goals:
        current = min(balance, goal.target_amount)
        current = max(current, 0)
        percentage = round((current / goal.target_amount) * 100, 1) if goal.target_amount > 0 else 0
        remaining = max(goal.target_amount - balance, 0)

        result.append(SavingsGoalWithProgress(
            id=goal.id,
            name=goal.name,
            target_amount=goal.target_amount,
            icon=goal.icon,
            current_amount=current,
            percentage=percentage,
            remaining=remaining
        ))

    return result

def create_goal(db: Session, data: SavingsGoalCreate, user_id: int):
    goal = SavingsGoal(
        name=data.name,
        target_amount=data.target_amount,
        icon=data.icon,
        user_id=user_id
    )
    db.add(goal)
    db.commit()
    db.refresh(goal)
    return goal

def delete_goal(db: Session, goal_id: int, user_id: int):
    goal = db.query(SavingsGoal).filter(
        SavingsGoal.id == goal_id,
        SavingsGoal.user_id == user_id
    ).first()
    if not goal:
        return False
    db.delete(goal)
    db.commit()
    return True