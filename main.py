from uvicorn import run
from src.app import app

from os import environ

PORT = int(environ.get("PORT", 8000))

run(app, host="0.0.0.0", port=PORT)