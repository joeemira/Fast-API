from fastapi import  Response,status,HTTPException,Depends,APIRouter
from .. import models,schemas
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db


router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)

@router.get("/",response_model=List[schemas.post_response])
async def get_posts(db:Session = Depends(get_db)):
    POSTS = db.query(models.POST).all()   
    return POSTS



@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.post_response)
async def submit_data(payload: schemas.post_create,db:Session = Depends(get_db)):  #make the Payload of the incoming 

    new_post = models.POST(**payload.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}")
def get_post(id:int,response:Response,db:Session = Depends(get_db)): # enforce that the API parameter is int and not any thing else  && get the response properties to add specific response code
    post = db.query(models.POST).filter(models.POST.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the post with id:{id} can't be found")
    return post


@router.delete("/{id}" ,status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db:Session = Depends(get_db)):
    post = db.query(models.POST).filter(models.POST.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the post with id:{id} can't be found")
    else:
        db.delete(post)
        db.commit()
        
    

@router.put("/{id}",status_code=status.HTTP_202_ACCEPTED)
def update_post(id :int ,payload:schemas.post_create ,db:Session = Depends(get_db)):
    
    query_post = db.query(models.POST).filter(models.POST.id == id)
    post = query_post.first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the post with id:{id} can't be found")
    
    query_post.update(payload.dict(),synchronize_session=False)    
    db.commit()
    db.refresh(post)
    return post


