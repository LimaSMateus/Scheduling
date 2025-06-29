from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongodb_uri: str
    mongodb_database: str

    model_config = {
        "env_file": ".env",
    }

def get_settings():
    return Settings()