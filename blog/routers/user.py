from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from .. import database, models, hashing, schemas
from ..repository import user

router = APIRouter(
    prefix="/user",
    tags=['User']
)
get_db = database.get_db
Hasher = hashing.Hasher


@router.post('/', response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return user.create(request=request, db=db)


@router.get('/', response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
    return user.show(id=id, db=db)