from datetime import datetime
import string
from pydantic import BaseModel ,EmailStr

from app.database import Base




class post_base(BaseModel): #extends the class  of the pydantic 
    title: str
    content : str
    published:bool =True  

class post_create(post_base):
    pass

class post_response(post_base):
    id: int
    created_at: datetime
    class config:       #it's not necessary to create a class in the updated version of pydantic 
        orm_mode = True
        
class user_base(BaseModel):
    email: EmailStr 
    password: str

class user_create(user_base):
    pass 

class user_response(BaseModel):
    id: int
    created_at: datetime
    email: EmailStr
    
    
class user_login(user_base):
    pass 