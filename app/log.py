import logging
import os
import sys

uvicorn_logger = logging.getLogger("uvicorn.error")
uvicorn_logger.propagate = False

logger = logging.getLogger(__name__)
if os.getenv("ENVIRONMENT") == "development":
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)


formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

# file_handler = logging.FileHandler('app.log')
# file_handler.setFormatter(formatter)

# logger.addHandler(file_handler)

# add stdout handler
# stream_handler = logging.StreamHandler(sys.stdout)
# stream_handler.setFormatter(formatter)
# logger.addHandler(stream_handler)

