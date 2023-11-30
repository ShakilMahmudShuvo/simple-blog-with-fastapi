from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas, models
from .database import engine, get_db
from sqlalchemy.orm import Session
from typing import List
from .hashing import Hasher
from .routers import blog, user

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(blog.router)
app.include_router(user.router)
