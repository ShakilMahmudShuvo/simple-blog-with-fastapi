from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session
from ..repository import blog


router = APIRouter(
    prefix="/blog",
    tags=['Blog']
)
get_db = database.get_db


@router.get('/', response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    print(blog.get_all(db))
    return blog.get_all(db)


@router.post('/', status_code=status.HTTP_201_CREATED, )
def create(request: schemas.Blog, db: Session = Depends(get_db),current_user: models.User = Depends(oauth2.get_current_user)):
    return blog.create(request, db)


@router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db),current_user: models.User = Depends(oauth2.get_current_user)):
    return blog.destroy(id, db)


@router.put('/', status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db),current_user: models.User = Depends(oauth2.get_current_user)):
    return blog.update(id,request,db)


@router.get('/', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def show(id: int, db: Session = Depends(get_db),current_user: models.User = Depends(oauth2.get_current_user)):
    return blog.show(id,db)
