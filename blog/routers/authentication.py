from fastapi import APIRouter, HTTPException, status, Depends
from .. import schemas, database, models
from sqlalchemy.orm import Session
from .. hashing import Hasher


router = APIRouter(
    tags=['Authentication']
)


@router.post("/login")
def login(request: schemas.Login, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if not Hasher.verify_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password")
    return user