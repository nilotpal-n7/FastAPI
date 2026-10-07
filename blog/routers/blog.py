from typing import List
from blog.database import get_db
from fastapi import APIRouter
from blog import schemas, models, oauth2
from sqlalchemy.orm import Session
from fastapi import Depends, status, Response, HTTPException

router = APIRouter(
    prefix="/blog",
    tags=['Blog'],
)

@router.post('/', status_code=status.HTTP_201_CREATED) # or you can manulallay give 201 ,now the status will be 201
def create(req: schemas.Blog, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    new_blog = models.Blog(title=req.title, body=req.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return {'detail': 'deleted'}

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, req: schemas.Blog, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    blog.update(req.model_dump())
    db.commit()
    return req

@router.get('/', response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    blogs = db.query(models.Blog).all()
    return blogs

@router.get('/{id}', status_code=200, response_model=schemas.ShowBlog)
def show(id, res: Response, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        # res.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail': f"Blog with id {id} is not available"}
        raise HTTPException(status_code=404, detail=f"Blog with id {id} is not available") # same thing
    return blog
