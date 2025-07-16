from pydantic_settings import BaseSettings, SettingsConfigDict
import os

env = os.getenv("APP_ENV", "development")
env_file = ".env.test" if env == "test" else ".env"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=env_file, extra="ignore")

    app_env: str = env

    database_name: str
    database_user: str
    database_password: str
    database_host: str
    database_port: int

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.database_user}:{self.database_password}@"
            f"{self.database_host}:{self.database_port}/{self.database_name}"
        )

settings = Settings() # type: ignore
