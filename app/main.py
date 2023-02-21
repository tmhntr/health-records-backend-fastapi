from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv(".env.dev")

from . import models, routes
from .database import engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(routes.router)


@app.get("/hello")
def read_root():
    return {"message": "World!"}
