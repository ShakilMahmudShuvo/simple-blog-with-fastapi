from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from .. import schemas, database, models
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/blog",
    tags=['Blog']
)
get_db = database.get_db


@router.get('/', response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@router.post('/', status_code=status.HTTP_201_CREATED, )
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with this id {id} is missing!')
    blog.delete(synchronize_session=False)
    db.commit()
    return 'done'


@router.put('/', status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with this id {id} is missing!')
    blog.update(request.dict())
    db.commit()
    return 'Update done'


@router.get('/', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def show(id: int, db: Session = Depends(get_db)):
    print("--------------")
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    creator = blog.creator
    if not blog:
        print("=========")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with this id {id} not found!")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detial': f"Blog with this id {id} not found!"}
    return blog.__dict__
