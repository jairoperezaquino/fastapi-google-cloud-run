from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader, APIKeyQuery
from app.config import settings

api_key_header = APIKeyHeader(name="x-api-key", auto_error=True)
api_key_query = APIKeyQuery(name="x-api-key", auto_error=True)


async def verify_api_key(api_key: str) -> str:
    if api_key != settings.api_key:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key


async def verify_api_key_header(api_key: str = Security(api_key_header)) -> str:
    return await verify_api_key(api_key)


async def verify_api_key_query(api_key: str = Security(api_key_query)) -> str:
    return await verify_api_key(api_key)
