from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    environment: str = "DEV"

    @property
    def is_prod(self) -> bool:
        return self.environment == "PROD"

    @property
    def is_dev(self) -> bool:
        return self.environment == "DEV"

settings = Settings()