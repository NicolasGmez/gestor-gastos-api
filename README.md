# Gastly API — Personal Finance Manager

REST API for Gastly, a personal finance web application. Built with FastAPI and PostgreSQL.

## Live

[API Documentation](https://gestor-gastos-api-bb5e.onrender.com/docs)

## Tech Stack

- **Framework:** FastAPI (Python)
- **Database:** PostgreSQL — Supabase
- **ORM:** SQLAlchemy
- **Auth:** JWT + bcrypt
- **Deployment:** Render

## Features

- JWT authentication with user registration and login
- Transactions and categories CRUD with expense/income classification
- Budget system per category with monthly spending tracking
- Savings goals with real-time progress based on current balance
- Financial summary endpoint with breakdown by category

## Running Locally

```bash
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Environment Variables

Copy `.env.example` and fill in your values.

## Related

[Gastly Frontend](https://gestor-gastos-frontend-chi.vercel.app/login)
