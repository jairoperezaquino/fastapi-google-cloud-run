import httpx
from fastapi.logger import logger
from typing import Optional


class AsyncHTTPClient:
    """
    A singleton wrapper for httpx.AsyncClient.
    Handles lifecycle (startup/shutdown) and provides a simple interface for publishing messages.
    Ensures only one instance exists across the entire application.
    """

    _instance: Optional["AsyncHTTPClient"] = None
    _client: Optional[httpx.AsyncClient] = None

    def __new__(cls):
        """Ensures only one instance of AsyncHTTPClient exists. Returns the singleton instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def start(self) -> None:
        """Initializes the httpx AsyncClient. Call this during FastAPI startup."""
        if self._client is not None:
            logger.warning(
                "httpx AsyncClient already initialized, skipping initialization"
            )
            return

        self._client = httpx.AsyncClient()
        logger.info(f"httpx AsyncClient started (id={id(self._client)})")

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


client = AsyncHTTPClient()
