from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "FastAPI"
    DOCS_URL: str | None = None
    REDOC_URL: str | None = None
    OPENAPI_URL: str = "/openapi.json"
    SCALAR_URL: str = "/scalar"

    DB_NAME: str = "postgres"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5431

    DB_CONNECTION_STR: str | None = None

    JWT_SECRET: str = "your-not-very-safe-secret"
    JWT_ALGORITHM: str = "HS256"
    JWT_TOKEN_EXPIRES: int = 60  # minutes

    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URL: str = "http://localhost:8000/auth/callback/google"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    def __init__(self, **kwargs):  # type: ignore
        super().__init__(**kwargs)  # type: ignore
        # Build connection string after env vars are loaded
        self.DB_CONNECTION_STR = (  # type: ignore
            f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings()
