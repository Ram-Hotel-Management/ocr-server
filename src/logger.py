import logging
import sys
from fastapi import Request

logger = logging.getLogger()

# formatter
formatter = logging.Formatter(fmt="%(asctime)s - %(levelname)s - %(message)s")

# handler
stream_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler('app.log')

file_handler.setFormatter(formatter)

logger.handlers = [file_handler]

logger.setLevel(logging.INFO)



async def log_request(req: Request, next):
    logger.info({
        'url': req.url.path,
        'method': req.method
    })

    res = await next(req)
    return res