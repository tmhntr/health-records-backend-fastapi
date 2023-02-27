from uvicorn import run
from src import app

from os import environ

PORT = int(environ.get("PORT", 8000))

if __name__ == "__main__":
    run(app, host="0.0.0.0", port=PORT)