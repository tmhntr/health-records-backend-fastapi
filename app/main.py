from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models, routes
from .database import engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(routes.router)

@app.get("/hello")
def read_root():
    return {"message": "World!"}
