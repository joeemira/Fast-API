from fastapi import FastAPI,Response,status,HTTPException,Depends
from pydantic import BaseModel
import psycopg2 
from psycopg2.extras import RealDictCursor
import time 
from . import models ,schemas ,utils
from.database import engine,SessionLocal ,get_db
from sqlalchemy.orm import Session 
from typing import List

models.Base.metadata.create_all(bind=engine)

app = FastAPI()



while True :
    try:
        conn = psycopg2.connect(host="localhost",database="fast-api",user='postgres',password="password",cursor_factory=RealDictCursor)
        Cursor=conn.cursor()
        print("the connection was succesful")
        break
    except Exception as error: 
        print("connection faild")
        
        print("the error", error)
        time.sleep(2)


@app.get("/")
async  def read_root():
    
    return {"Hello": "world"}

@app.get("/posts",response_model=List[schemas.post_response])
async def get_posts(db:Session = Depends(get_db)):
    POSTS = db.query(models.POST).all()   
    return POSTS



@app.post("/posts",status_code=status.HTTP_201_CREATED,response_model=schemas.post_response)
async def submit_data(payload: schemas.post_create,db:Session = Depends(get_db)):  #make the Payload of the incoming 

    new_post = models.POST(**payload.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get("/posts/{id}")
def getpost(id:int,response:Response,db:Session = Depends(get_db)): # enforce that the API parameter is int and not any thing else  && get the response properties to add specific response code
    post = db.query(models.POST).filter(models.POST.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the post with id:{id} can't be found")
    return post



@app.delete("/posts/{id}" ,status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db:Session = Depends(get_db)):
    post = db.query(models.POST).filter(models.POST.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the post with id:{id} can't be found")
    
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT) 





@app.put("/posts/{id}",status_code=status.HTTP_202_ACCEPTED)
def update_post(id :int ,payload:schemas.post_create ,db:Session = Depends(get_db)):
    
    query_post = db.query(models.POST).filter(models.POST.id == id)
    post = query_post.first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the post with id:{id} can't be found")
    
    query_post.update(payload.dict(),synchronize_session=False)    
    db.commit()
    db.refresh(post)
    return post



### creating users 

@app.post("/users",status_code=status.HTTP_201_CREATED,response_model=schemas.user_response)
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
    
    
@app.get("/users/{id}",response_model=schemas.user_response)
def get_user(id:int,db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the user with id:{id} can't be found")
    return user 