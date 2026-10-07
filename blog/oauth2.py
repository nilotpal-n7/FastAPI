from fastapi import Depends
from blog.jwt import verify_token
from fastapi.security import OAuth2PasswordBearer

oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_schema)):
    return verify_token(token)
