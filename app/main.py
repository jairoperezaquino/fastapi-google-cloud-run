from fastapi import FastAPI
from fastapi.logger import logger

from app.config import settings
from app.logging.setup import setup_logging

app = FastAPI()
setup_logging(app)


@app.get("/")
async def root():
    logger.debug("DEBUG LOG")
    logger.error("ERROR LOG")
    logger.warning("WARNING LOG")
    logger.info("INFO LOG")
    return {"message": "Hello World", "environment": settings.environment}
