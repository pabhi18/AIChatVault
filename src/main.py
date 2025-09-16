from fastapi import APIRouter, FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from src.database import get_db
from contextlib import asynccontextmanager
from src.database import get_db, User, RequestLog, create_tables
from src.auth import get_current_user, User, get_password_hash
from src.routers import auth as auth_router, ai_service as ai_router, admin_func as admin_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    print("✅ Tables created and DB ready!")
    yield
    print("👋 App is shutting down...")

app = FastAPI(lifespan=lifespan)

app.include_router(auth_router.router)
app.include_router(ai_router.router)
app.include_router(admin_router.router)

@app.get("/")
def main(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        db_status = "Connected ✅"
    except Exception as e:
        db_status = f"Not connected ❌: {str(e)}"
    
    return {
        "message": "Welcome to the AI Auth API!",
        "database_status": db_status
    }