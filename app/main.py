from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models, routes
from .database import engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# origins = [
#     "http://localhost",
#     "http://localhost:8080",
#     "http://localhost:8081",
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

app.include_router(routes.router)

@app.get("/hello")
def read_root():
    return {"message": "World!"}
