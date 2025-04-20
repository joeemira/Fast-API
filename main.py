from sqlite3 import Cursor
from sys import exception
from turtle import pos
from typing import Optional, Union
from urllib import response
from fastapi import FastAPI,Response,status,Body,HTTPException
from fastapi.exception_handlers import http_exception_handler
from pydantic import BaseModel
from random import randrange
import psycopg2 
from psycopg2.extras import RealDictCursor
import time 

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







@app.get("/login")
async  def read_root():
    
    return {"Hello": "world"}

@app.get("/posts")
async def get_posts():
    Cursor.execute("""SELECT * FROM public.posts""")
    DATA = Cursor.fetchall()    
    return {"data": DATA}

class post(BaseModel): #extends the class  of the pydantic 
    title: str
    content : str
    published:bool =True  #default input iff not passed don't true error 
    rating: Optional[int] = None 
    # id:Optional[int] 
    

     
@app.post("/posts",status_code=status.HTTP_201_CREATED)
async def submit_data(payload: post):  #make the Payload of the incoming 
    

    Cursor.execute("""INSERT INTO posts(title,content,published) VALUES (%s,%s,%s) RETURNING * """  ,(payload.title,payload.content,payload.published)) #using prepared statement instead of f string mitigate the code from SQL I 
    new_post = Cursor.fetchone()
    conn.commit() #to save the changes into the db 
    return {"received":new_post}


@app.get("/posts/{id}")
def getpost(id:int,response:Response): # enforce that the API parameter is int and not any thing else  && get the response properties to add specific response code
    Cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id,) ) 
    fetched_posts = Cursor.fetchone()
    if fetched_posts := Cursor.fetchone():
        return {"post": fetched_posts}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id :{id} was not found")


@app.delete("/posts/{id}" ,status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    Cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *  """,(id,))
    deleted_post = Cursor.fetchone()
    conn.commit()
    if  deleted_post is None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the post with id:{id} can't be found")
    
    
@app.put("/posts/{id}",status_code=status.HTTP_202_ACCEPTED)
def update_post(id :int ,payload:post):

    Cursor.execute("""UPDATE posts SET title=%s,content=%s,published=%s where id =%s RETURNING *""",(payload.title,payload.content,payload.published,id))
    updated_post = Cursor.fetchone()
    conn.commit()
    if updated_post is None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the post with id:{id} can't be found ")
    
    else:
        return {"message": "Post updated", "post": updated_post}
    