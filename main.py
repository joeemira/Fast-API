from fastapi import FastAPI,Response,status,HTTPException,Depends
import psycopg2 
from psycopg2.extras import RealDictCursor
import time 
from . import models ,schemas ,utils
from.database import engine,SessionLocal ,get_db
from sqlalchemy.orm import Session 
from .routers import user ,posts,auth

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




app.include_router(user.router)
app.include_router(posts.router)        
app.include_router(auth.router)
