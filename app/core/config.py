"""
Configuración centralizada del proyecto (buenas prácticas).

- Carga variables desde .env
- Evita valores hardcoded
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Voting API"
    database_url: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
