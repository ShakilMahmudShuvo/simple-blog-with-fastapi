from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException, status


def get_all(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs


def create(request: schemas.Blog, db: Session):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def destroy(id: int, db: Session):
    blogs = db.query(models.Blog).filter(models.Blog.id == id)
    if not blogs.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog does not exist")

    blogs.delete(synchronize_session=False)
    db.commit()
    return 'Deleted Blog successfully'


def update(id: int, request: schemas.Blog, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with this id {id} is missing!')
    blog.update(request.dict())
    db.commit()
    return 'Update done'


def show(id: int, db: Session):
    print("--------------")
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    creator = blog.creator
    if not blog:
        print("=========")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with this id {id} not found!")
        # response.status_co de = status.HTTP_404_NOT_FOUND
        # return {'detial': f"Blog with this id {id} not found!"}
    return blog.__dict__
