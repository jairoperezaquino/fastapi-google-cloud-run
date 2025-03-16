from fastapi import FastAPI
from fastapi.logger import logger
import logging

from app.config import settings
from app.logging.google.setup import setup_google_logging
from app.logging.google.middleware import LoggingMiddleware



def setup_local_logging():
    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


def setup_logging(app: FastAPI):
    setup_local_logging() if settings.is_local else setup_google_logging(app)

def setup_logging_middleware(app: FastAPI):
    app.add_middleware(LoggingMiddleware)