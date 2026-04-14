from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.models import user, category, transaction
from app.models import budget
from app.routers import auth, categories, transactions, budgets

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Gestor de Gastos API",
    description="API para gestión de gastos personales",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(transactions.router)
app.include_router(budgets.router)

@app.get("/")
def root():
    return {"message": "Gestor de Gastos API funcionando"}