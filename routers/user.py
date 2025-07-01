
from fastapi import status,HTTPException,Depends,APIRouter
from .. import models,schemas,utils
from sqlalchemy.orm import Session
from ..database import get_db


router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.user_response)
def create_user(user:schemas.user_create,db:Session = Depends(get_db)):
    user.password = utils.hash(user.password)
    new_user = models.User(**user.dict())
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception :
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="user already exists")
    
    
@router.get("/{id}",response_model=schemas.user_response)
def get_user(id:int,db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the user with id:{id} can't be found")
    return user 