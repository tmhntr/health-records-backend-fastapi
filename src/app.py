import os
from fastapi import FastAPI

import src.resources.record.router as record_route
import src.resources.user.router as user_route
from src.database import engine, Base


from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.cors import CORSMiddleware


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.debug = os.environ.get("DEBUG", False)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8080",
    "http://localhost:8081",
    "https://dev-mx-lf095.us.auth0.com",
    "https://health.timhunterdev.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionMiddleware,
                   secret_key="some-random-string", max_age=None)
app.add_middleware(CORSMiddleware, allow_origins=origins,
                   allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# app.include_router(routes.auth.router)
app.include_router(record_route.router)
app.include_router(user_route.router)
