from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.models import user, category, transaction
from app.routers import auth, categories, transactions

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Gestor de Gastos API",
    description="API para gestión de gastos personales",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(transactions.router)

@app.get("/")
def root():
    return {"message": "Gestor de Gastos API funcionando"}