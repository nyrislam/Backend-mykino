from fastapi import FastAPI, Response, status, HTTPException, Depends
from typing import List
from . import models, schemas, utils
from .database import engine, Session, get_db
from .settings import setup_cors
from .routers import users, auth, wishlists
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
setup_cors(app)


@app.get('/')
def root():
    return {'data':"hello world"}

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(wishlists.router)
