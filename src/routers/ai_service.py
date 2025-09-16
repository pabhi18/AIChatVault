from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from src.database import get_db, User, RequestLog
import src.ai_service as ai_utils, src.auth as auth_utils
from src.schemas import ChatRequest, ChatResponse

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/", response_model=ChatResponse)
def chat_with_ai(
    payload: ChatRequest,
    request: Request,
    current_user: User = Depends(ai_utils.get_current_user),  
    db: Session = Depends(get_db)
):
    ip_address = request.client.host
    if current_user is None:
        request_count = db.query(RequestLog).filter(
            RequestLog.ip_address == ip_address
        ).count()

        if request_count >= 5:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Guest users can only make 5 requests. Please log in for unlimited access."
            )
        
    if current_user and not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )

    response = ai_utils.get_ai_response(payload.message, ip_address, current_user, db)
    if response is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="AI service error"
        )
    log_entry = RequestLog(
        user_id=current_user.id if current_user else None,
        ip_address=ip_address if current_user is None else None,
        prompt=payload.message,
        response=response["generated_text"],
        request_count = payload.request_count
    )
    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)

    return ChatResponse(response=response["generated_text"])