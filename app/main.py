from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.logger import logger
from contextlib import asynccontextmanager

from app.config import settings
from app.http import client as http_client
from app.auth import verify_api_key_header, verify_api_key_query
from app.logging.setup import setup_logging, setup_logging_middleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    setup_logging(app)
    http_client.start()
    yield
    await http_client.stop()


app = FastAPI(lifespan=lifespan)
setup_logging_middleware(app)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint with logging examples."""
    logger.debug("DEBUG LOG")
    logger.error("ERROR LOG")
    logger.warning("WARNING LOG")
    logger.info("INFO LOG")
    return {"message": "Hello World", "environment": settings.environment}


@app.get("/auth/header")
async def header_auth(api_key: str = Depends(verify_api_key_header)):
    """Example endpoint with header-based API key auth."""
    return {
        "message": "Authenticated",
        "api_key": api_key,
        "environment": settings.environment,
    }


@app.get("/auth/query")
async def query_auth(api_key: str = Depends(verify_api_key_query)):
    """Example endpoint with query parameter API key auth."""
    return {
        "message": "Authenticated",
        "api_key": api_key,
        "environment": settings.environment,
    }
