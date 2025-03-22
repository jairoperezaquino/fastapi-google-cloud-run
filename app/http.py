import httpx
from fastapi.logger import logger
from typing import Optional


class AsyncHTTP:
    """
    A singleton wrapper for httpx.AsyncClient.
    Handles lifecycle (startup/shutdown) and ensures one shared instance across the app.
    """

    _instance: Optional["AsyncHTTP"] = None
    _client: Optional[httpx.AsyncClient] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def start(self) -> None:
        """Initializes the AsyncClient. Call this during FastAPI startup."""
        if self._client is None:
            self._client = httpx.AsyncClient()
            logger.info(f"httpx AsyncClient started (id={id(self._client)})")
        else:
            logger.debug("httpx AsyncClient already initialized.")

    async def stop(self) -> None:
        """Closes the AsyncClient. Call this during FastAPI shutdown."""
        if self._client:
            await self._client.aclose()
            logger.info("httpx AsyncClient closed.")
            self._client = None

    def get_client(self) -> httpx.AsyncClient:
        """Returns the active httpx.AsyncClient instance."""
        if self._client is None:
            raise RuntimeError("AsyncHTTP client not started. Call `.start()` first.")
        if self._client.is_closed:
            raise RuntimeError(
                "AsyncHTTP client is closed. Call `.start()` to reinitialize."
            )
        return self._client


async_http = AsyncHTTP()
