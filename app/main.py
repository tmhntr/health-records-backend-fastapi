from fastapi import FastAPI

from app import models, routes
from app.database import engine
from app import env

from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.cors import CORSMiddleware


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.debug = True

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8080",
    "http://health.timhunterdev.com"
]

app.add_middleware(SessionMiddleware, secret_key="some-random-string", max_age=None)
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.include_router(routes.auth.router)
app.include_router(routes.records.router)
app.include_router(routes.users.router)


# @app.middleware("http")
# async def add_process_time_header(request, call_next):
#     response = await call_next(request)
#     response.headers["X-Process-Time"] = "42ms"
#     return response

# @app.middleware("http")
# async def get_user_from_session(request, call_next):
#     request.state.user = request.session.get("user")
#     response = await call_next(request)
#     return response
