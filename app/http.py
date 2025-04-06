import httpx
from fastapi.logger import logger
from typing import Optional, Any


class AsyncHTTPClient:
    """
    A singleton wrapper for httpx.AsyncClient.
    Handles lifecycle (startup/shutdown) and provides a simple interface for publishing messages.
    Ensures only one instance exists across the entire application.
    """

    _instance: Optional["AsyncHTTPClient"] = None
    _client: Optional[httpx.AsyncClient] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def start(self) -> None:
        """Initialize the httpx AsyncClient."""
        if self._client is not None:
            logger.warning("httpx AsyncClient already initialized")
            return

        self._client = httpx.AsyncClient()
        logger.info("httpx AsyncClient started")

    async def stop(self) -> None:
        """Close the AsyncClient."""
        if self._client:
            await self._client.aclose()
            logger.info("httpx AsyncClient closed")
            self._client = None

    def get_client(self) -> httpx.AsyncClient:
        """Return the active httpx.AsyncClient instance."""
        if self._client is None:
            raise RuntimeError("AsyncHTTP client not started")
        if self._client.is_closed:
            raise RuntimeError("AsyncHTTP client is closed")
        return self._client

    async def request(self, method: str, url: str, **kwargs: Any) -> httpx.Response:
        """Make an HTTP request."""
        client = self.get_client()
        try:
            response = await client.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except httpx.HTTPError as e:
            logger.error(f"HTTP request failed: {str(e)}")
            raise


client = AsyncHTTPClient()
