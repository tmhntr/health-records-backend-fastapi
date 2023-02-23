import logging
import sys

from uvicorn.config import LOGGING_CONFIG
from uvicorn.logging import DefaultFormatter
from app.env import env

uvicorn_logger = logging.getLogger("uvicorn.error")
uvicorn_logger.propagate = False
logging.getLogger("uvicorn.access").propagate = False

logger = logging.getLogger(__name__)
print("LOGGING_CONFIG", LOGGING_CONFIG)
# logging.basicConfig(**LOGGING_CONFIG)
if env.get("ENVIRONMENT") == "development":
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

# file_handler = logging.FileHandler('app.log')
# file_handler.setFormatter(formatter)

# logger.addHandler(file_handler)
options = LOGGING_CONFIG.get("formatters", {}).get("uvicorn.access", {})
options.pop("()", None)
formatter = DefaultFormatter(**options, use_colors=True)

# add stdout handler
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

