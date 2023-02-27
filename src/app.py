import os
from fastapi import FastAPI

import src.models as models
import src.routes as routes
from src.database import engine


from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.cors import CORSMiddleware


models.Base.metadata.create_all(bind=engine)

# def create_tables():
#     try:
#     except Exception as e:
#         print(e)

# create_tables()


app = FastAPI()

app.debug = os.environ.get("DEBUG", False)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8080",
    "http://localhost:8081",
    "https://dev-mx-lf095.us.auth0.com",
    "http://health.timhunterdev.com"
]

app.add_middleware(SessionMiddleware, secret_key="some-random-string", max_age=None)
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# app.include_router(routes.auth.router)
app.include_router(routes.records.router)
app.include_router(routes.users.router)


