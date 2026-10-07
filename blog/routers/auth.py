from blog.hashing import Hash
from blog.database import get_db
from fastapi import APIRouter
from blog import models
from sqlalchemy.orm import Session
from blog.jwt import create_access_token
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix='/auth',
    tags=['Auth'],
)

@router.post('/login')
def login(req: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == req.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials: u")
    if Hash.verify(req.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials: p")
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
