from sqlalchemy.orm import Session
from app.models.user import User
from app.models.category import Category, CategoryType
from app.schemas.user import UserCreate
from app.core.security import hash_password, verify_password, create_access_token

DEFAULT_CATEGORIES = [
    {"name": "Comida", "color": "#f59e0b", "type": CategoryType.expense},
    {"name": "Transporte", "color": "#3b82f6", "type": CategoryType.expense},
    {"name": "Servicios del hogar", "color": "#8b5cf6", "type": CategoryType.expense},
    {"name": "Diversión", "color": "#ec4899", "type": CategoryType.expense},
    {"name": "Salud", "color": "#10b981", "type": CategoryType.expense},
    {"name": "Ropa", "color": "#f97316", "type": CategoryType.expense},
    {"name": "Educación", "color": "#06b6d4", "type": CategoryType.expense},
    {"name": "Salario", "color": "#22c55e", "type": CategoryType.income},
    {"name": "Préstamo recibido", "color": "#64748b", "type": CategoryType.income},
    {"name": "Ingreso extra", "color": "#a855f7", "type": CategoryType.income},
    {"name": "Freelance", "color": "#0ea5e9", "type": CategoryType.income},
]

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()

def create_default_categories(db: Session, user_id: int):
    for cat in DEFAULT_CATEGORIES:
        category = Category(
            name=cat["name"],
            color=cat["color"],
            type=cat["type"],
            user_id=user_id
        )
        db.add(category)
    db.commit()

def create_user(db: Session, user_data: UserCreate) -> User:
    hashed = hash_password(user_data.password)
    user = User(
        email=user_data.email,
        hashed_password=hashed,
        full_name=user_data.full_name
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    create_default_categories(db, user.id)
    return user

def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def login_user(db: Session, email: str, password: str) -> dict | None:
    user = authenticate_user(db, email, password)
    if not user:
        return None
    token = create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}