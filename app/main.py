import logging
from fastapi.logger import logger
from app.cloud_logging.middleware import LoggingMiddleware
from app.cloud_logging.setup import setup_logging

from fastapi import FastAPI
from pydantic_settings import BaseSettings

class Setttings(BaseSettings):
    environment: str = "DEV"

settings = Setttings()
app = FastAPI()

if settings.environment == "PROD":
    setup_logging()
    app.add_middleware(LoggingMiddleware)
else:
    # TODO: setup local logging - it's only printing ERROR and WARNING logs
    logger.setLevel(logging.DEBUG)


@app.get("/")
async def root():
    logger.debug('DEBUG LOG')
    logger.error('ERROR LOG')
    logger.warning('WARNING LOG')
    logger.info('INFO LOG')
    return {'message': 'Hello World', 'environment': settings.environment}