import logging
from uvicorn import run
from src.app import app
import os

from os import environ

PORT = int(environ.get("PORT", 8000))

uvicorn_logger = logging.getLogger("uvicorn.error")
uvicorn_logger.propagate = False

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG if os.environ.get("DEBUG", False) else logging.INFO)

run(app, host="0.0.0.0", port=PORT)