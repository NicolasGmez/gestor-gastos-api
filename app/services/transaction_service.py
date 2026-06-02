from sqlalchemy.orm import Session
from app.models.category import Category
from app.models.transaction import Transaction
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.schemas.transaction import TransactionCreate, TransactionUpdate

def get_categories(db: Session, user_id: int):
    return db.query(Category).filter(Category.user_id == user_id).all()

def get_category(db: Session, category_id: int, user_id: int):
    return db.query(Category).filter(
        Category.id == category_id,
        Category.user_id == user_id
    ).first()

def create_category(db: Session, data: CategoryCreate, user_id: int):
    category = Category(**data.model_dump(), user_id=user_id)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

def update_category(db: Session, category_id: int, data: CategoryUpdate, user_id: int):
    category = get_category(db, category_id, user_id)
    if not category:
        return None
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(category, key, value)
    db.commit()
    db.refresh(category)
    return category

def delete_category(db: Session, category_id: int, user_id: int):
    category = get_category(db, category_id, user_id)
    if not category:
        return False
    db.delete(category)
    db.commit()
    return True

def get_transactions(db: Session, user_id: int):
    return db.query(Transaction).filter(
        Transaction.user_id == user_id
    ).order_by(Transaction.date.desc()).all()

def get_transaction(db: Session, transaction_id: int, user_id: int):
    return db.query(Transaction).filter(
        Transaction.id == transaction_id,
        Transaction.user_id == user_id
    ).first()

def create_transaction(db: Session, data: TransactionCreate, user_id: int):
    transaction = Transaction(**data.model_dump(), user_id=user_id)
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction

def update_transaction(db: Session, transaction_id: int, data: TransactionUpdate, user_id: int):
    transaction = get_transaction(db, transaction_id, user_id)
    if not transaction:
        return None
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(transaction, key, value)
    db.commit()
    db.refresh(transaction)
    return transaction

def delete_transaction(db: Session, transaction_id: int, user_id: int):
    transaction = get_transaction(db, transaction_id, user_id)
    if not transaction:
        return False
    db.delete(transaction)
    db.commit()
    return True

def create_transactions_bulk(db: Session, transactions_data: list[TransactionCreate], user_id: int):
    if not transactions_data:
        return []

    first_type = transactions_data[0].type

    for item in transactions_data:
        if item.type != first_type:
            raise ValueError("Todas las transacciones deben ser del mismo tipo")

    transactions = [
        Transaction(**item.model_dump(), user_id=user_id)
        for item in transactions_data
    ]

    db.add_all(transactions)
    db.commit()

    for transaction in transactions:
        db.refresh(transaction)

    return transactions