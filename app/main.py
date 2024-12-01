import logging
from fastapi.logger import logger
from cloud_logging.middleware import LoggingMiddleware
from cloud_logging.setup import setup_logging

from fastapi import FastAPI
from pydantic_settings import BaseSettings

class Setttings(BaseSettings):
    environment: str = "development"

settings = Setttings()
app = FastAPI()

if settings.environment == "production":
    setup_logging()
    app.add_middleware(LoggingMiddleware)
else:
    logger.setLevel(logging.DEBUG)


@app.get("/")
async def root():
    logger.debug('DEBUG LOG')
    logger.error('ERROR LOG')
    logger.warning('WARNING LOG')
    logger.info('INFO LOG')
    return {'message': 'Hello World'}