import logging
from app.env import env

uvicorn_logger = logging.getLogger("uvicorn.error")
uvicorn_logger.propagate = False

logger = logging.getLogger(__name__)
if env.get("ENVIRONMENT") == "development":
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

# file_handler = logging.FileHandler('app.log')
# file_handler.setFormatter(formatter)

# logger.addHandler(file_handler)

# add stdout handler
# stream_handler = logging.StreamHandler(sys.stdout)
# stream_handler.setFormatter(formatter)
# logger.addHandler(stream_handler)

