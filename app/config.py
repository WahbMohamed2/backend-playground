from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str
    DATABASE_URL: str
    CLERK_JWKS_URL: str
    CLERK_SECRET_KEY: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
