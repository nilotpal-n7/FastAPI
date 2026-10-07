from blog.hashing import Hash
from blog.database import get_db
from fastapi import APIRouter
from blog import schemas, models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException

router = APIRouter(
    prefix="/user",
    tags=['User'],
)

@router.post('/', response_model=schemas.ShowUser)
def create_user(req: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name=req.name, email=req.email, password=Hash.bcrypt(req.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{id}', response_model=schemas.ShowUser)
def show_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {id} is not available")
    return user
