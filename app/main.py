from fastapi import FastAPI
from fastapi.logger import logger
from contextlib import asynccontextmanager

from app.config import settings
from app.http import async_http
from app.logging.setup import setup_logging, setup_logging_middleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging(app)
    async_http.start()
    yield
    logger.info("Shutting down")
    await async_http.stop()


app = FastAPI(lifespan=lifespan)
setup_logging_middleware(app)


@app.get("/")
async def root():
    logger.debug("DEBUG LOG")
    logger.error("ERROR LOG")
    logger.warning("WARNING LOG")
    logger.info("INFO LOG")
    return {"message": "Hello World", "environment": settings.environment}
