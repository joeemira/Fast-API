from sqlite3 import Cursor
from sys import exception
from typing import Optional, Union
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








# My_Posts=[{"title":"title of post 1","content":"content of post1","id":1 },{"title":"title of post 2","content":"content of post2","id":2 }]



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
    
    # # print(payload.dict())  #accessing the built in method convert to dict in pydantic 
    # post_dict=payload.dict()
    # post_dict['id']=randrange(0,1000000)
    # My_Posts.append(post_dict) 
    Cursor.execute("""INSERT INTO posts(title,content,published) VALUES (%s,%s,%s) RETURNING * """  ,(payload.title,payload.content,payload.published)) #using prepared statement instead of f string mitigate the code from SQL I 
    new_post = Cursor.fetchone()
    conn.commit() #to save the changes into the db 
    return {"received":new_post}


# def get_post(id):
#     for x in My_Posts:
#         if x['id'] == id:
#             return x
        
# def get_post(ID):
#     Cursor.execute("""SELECT * FROM posts WHERE id = %s""", (ID,) ) 
#     if not (returned_post := Cursor.fetchone()):
#         return False
#     else:
#         return returned_post
        
        


@app.get("/posts/{id}")
def getpost(id:int,response:Response): # enforce that the API parameter is int and not any thing else  && get the response properties to add specific response code
    # post = get_post(id)
    # if not post:
    #     # response.status_code =status.HTTP_404_NOT_FOUND
    #     # return {"message":f"post with id:{id} was not found"}
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"post with id:{id} was not found")
    # return post
    Cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id,) ) 
    r_post = Cursor.fetchone()
    if not r_post :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id :{id} was not found")
    return {"post" : r_post}


''
def find_post(id: int):
    for i, p in enumerate(My_Posts):
        if p["id"] == id:
            return i
        return None

@app.delete("/posts/{id}" ,status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post_id = find_post(id)
    if post_id is not None: 
        My_Posts.pop(post_id)
        return {"message": "Your post has been deleted"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the post with id:{id} can't be found ")
    


    
    
@app.put("/posts/{id}")
def update_post(id :int ,payload:post):
    post_id = find_post(id)
    if post_id is  None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the post with id:{id} can't be found ")
    
    post_dict =payload.dict()
    post_dict["id"]=id
    My_Posts[post_id]= post_dict
    
    return {"message": "Post updated", "post": post_dict}
     
     
     
