from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    environment: Literal["PROD", "DEV", "LOCAL"] = "LOCAL"
    api_key: str

    @property
    def is_prod(self) -> bool:
        return self.environment == "PROD"

    @property
    def is_dev(self) -> bool:
        return self.environment == "DEV"

    @property
    def is_local(self) -> bool:
        return self.environment == "LOCAL"

    class Config:
        env_file = ".env"


settings = Settings()
