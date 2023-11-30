from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from .. import database, models, hashing, schemas


router = APIRouter(
    prefix="/user",
    tags=['User']
)
get_db = database.get_db
Hasher = hashing.Hasher


@router.post('/', response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    hashed_password = Hasher.bcrypt_hash(request.password)
    new_user = models.User(name=request.name, email=request.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/', response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with this id {id} is not available!")
    return user