from fastapi import Depends, HTTPException, status
from transformers import pipeline
from sqlalchemy.orm import Session
from src.database import get_db, RequestLog, User
import src.auth as auth_utils
from typing import Optional

def load_model():
    model = "openai-community/gpt2"
    return pipeline("text-generation", model=model)

def generate_text(generator, prompt):
    result = generator(
        prompt,
        max_new_tokens=50,
        num_return_sequences=1
    )
    return {"generated_text": result[0]["generated_text"]}

def log_request(db: Session, user_id: Optional[int], ip_address: str, prompt: str, response: str):
    log_entry = RequestLog(
        user_id=user_id,
        ip_address=ip_address,
        prompt=prompt,
        response=response
    )
    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)
    return log_entry

model_pipeline = load_model()

def get_ai_response(
    prompt: str,
    ip_address: str,
    current_user: Optional[User] = Depends(auth_utils.get_current_user),
    db: Session = Depends(get_db)
):
    user_id = current_user.id if current_user else None

    # Validate user first
    if current_user and not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user"
        )

    response = generate_text(model_pipeline, prompt)
    log_request(db, user_id, ip_address, prompt, response["generated_text"])

    return response

def get_current_user( token: str = Depends(auth_utils.oauth2_scheme), db: Session = Depends(get_db)) -> Optional[User]:
    if not token:  
        return None
    try:
        return auth_utils.get_current_user(token, db)
    except HTTPException:
        return None



