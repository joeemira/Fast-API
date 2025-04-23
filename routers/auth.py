from fastapi import APIRouter, Depends , status, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db



router = APIRouter(
    
    tags=["auth"]
)

@router.post("/login")
def login(user_credentials: schemas.user_login, db: Session = Depends(get_db)):
    user =db.query(models.User).filter(models.User.email == user_credentials.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_FORBIDDEN,detail=f"invalid credentials")
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"invalid credentials")
    
    return {"access_token":user.id }