from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database import get_db, User, RequestLog
import src.auth as auth_utils

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    include_in_schema=False,
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(auth_utils.get_admin_user)]
)

@router.patch("/users/{user_id}/deactivate")
def deactivate_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    user.is_active = False
    db.commit()
    db.refresh(user)
    
    return {"message": f"User {user.username} has been deactivated."}

@router.patch("/users/{user_id}/reactivate")
def reactivate_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    user.is_active = True
    db.commit()
    db.refresh(user)
    
    return {"message": f"User {user.username} has been reactivated."}

@router.delete("/delete-user/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)): 
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    db.delete(user)
    db.commit()
    
    return {"message": f"User {user.username} has been deleted."}

@router.delete("/delete_logs")
def delete_all_logs(db: Session = Depends(get_db)):
    deleted = db.query(RequestLog).delete()
    db.commit()
    return {"message": f"Deleted {deleted} log entries."}   

@router.get("/users")
def get_users_details(db: Session = Depends(get_db)):
    users = db.query(User).all()
    user_list = [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_active": user.is_active
        }
        for user in users
    ]
    return {"users": user_list}

@router.get("/logs")
def get_request_logs(db: Session = Depends(get_db)):
    logs = db.query(RequestLog).all()
    log_list = [
        {
            "id": log.id,
            "user_id": log.user_id,
            "ip_address": log.ip_address,
            "prompt": log.prompt,
            "response": log.response,
            "timestamp": log.timestamp
        }
        for log in logs
    ]
    return {"logs": log_list}

@router.get("/users/{user_id}")
def get_user_detail(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    logs = db.query(RequestLog).filter(RequestLog.user_id == user_id).all()
    
    user_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "is_active": user.is_active,
        "created_at": user.created_at,
    }

    user_logs = {
        "logs": [
            {
                "id": log.id,
                "ip_address": log.ip_address,
                "prompt": log.prompt,
                "response": log.response,
                "timestamp": log.timestamp
            }
            for log in logs
        ]
    }

    return {"user": user_data, "logs": user_logs}
