import logging
from fastapi.logger import logger
from app.cloud_logging.middleware import LoggingMiddleware
from app.cloud_logging.setup import setup_logging

from fastapi import FastAPI
from app.config import settings


app = FastAPI()

if settings.is_prod:
    setup_logging()
    app.add_middleware(LoggingMiddleware)
else:
    # Setup local logging 
    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


@app.get("/")
async def root():
    logger.debug("DEBUG LOG")
    logger.error("ERROR LOG")
    logger.warning("WARNING LOG")
    logger.info("INFO LOG")
    return {"message": "Hello World", "environment": settings.environment}
