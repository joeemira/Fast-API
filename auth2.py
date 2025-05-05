from jose import    jwt
from datetime import datetime, timedelta

SECRET_KEY = "welcome"
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 1



def create_access_token(data: dict):
    to_encode = data.copy()
    expire=datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt