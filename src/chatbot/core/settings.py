from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    UPLOAD_DIR: str ="uploads"


settings = Settings()