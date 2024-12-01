import logging
from fastapi.logger import logger
from cloud_logging.middleware import LoggingMiddleware
from cloud_logging.setup import setup_logging

import logging
from fastapi import FastAPI

app = FastAPI()

setup_logging()
app.add_middleware(LoggingMiddleware)

@app.get("/")
async def root():
    logger.debug('DEBUG LOG')
    logger.error('ERROR LOG')
    logger.warning('WARNING LOG')
    logger.info('INFO LOG')
    return {'message': 'Hello World'}