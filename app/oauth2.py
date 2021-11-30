from fastapi import Depends,status,HTTPException
from jose import JWTError,jwt
from datetime import datetime,timedelta
from sqlalchemy.orm.session import Session
from . import schemas,database,models
from fastapi.security import OAuth2PasswordBearer
from .config import settings

oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

JWT_SECRET = settings.SECRET_KEY

ALGORITHM = settings.ALGORITHM

ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(data:dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({'exp':expire})

    encoded_jwt = jwt.encode(to_encode,JWT_SECRET,algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token:str,credentials_exception):

    try:
        payload = jwt.decode(token,JWT_SECRET,algorithms=[ALGORITHM])

        id = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data
    

def get_current_user(token:str = Depends(oauth2_schema),db:Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials",
    headers={"WWW-Authenticate":"Bearer"})


    token = verify_access_token(token,credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user