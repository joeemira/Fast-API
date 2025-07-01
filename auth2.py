from jose import    JWTError, jwt
from datetime import datetime, timedelta
from . import schemas
SECRET_KEY = "welcome"
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 1



def create_access_token(data: dict):
    to_encode = data.copy()
    expire=datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token:str, credintials_exeption):
    try:
        payload= jwt.decode(token,SECRET_KEY,ALGORITHM)
        id = payload.get("user_id")

        if id is None:
            raise credintials_exeption
        token_data = schemas.TokenData(id=id)
        return token_data

    except JWTError:
        raise credintials_exeption
    