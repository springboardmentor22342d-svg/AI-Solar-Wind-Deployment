"""
app/config.py – Application configuration using Pydantic Settings.

Pydantic Settings reads values from the .env file automatically.
All settings are strongly-typed and validated at startup.

Task: Backend Foundation – Configuration Module
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import json


class Settings(BaseSettings):
    """
    Central configuration object.
    Values are loaded from .env file via python-dotenv / pydantic-settings.
    """

    APP_NAME: str = "Solar & Wind Deployment Intelligence Platform"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    SECRET_KEY: str = "change-me-in-production-minimum-32-characters"

    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/solar_wind_db"
    POSTGRES_DB: str = "solar_wind_db"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432

    JWT_SECRET_KEY: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174"
    ]

    NASA_POWER_DATA_PATH: str = "datasets/nasa_power"
    GLOBAL_WIND_ATLAS_PATH: str = "datasets/global_wind_atlas"
    SENTINEL_PATH: str = "datasets/sentinel"
    OSM_PATH: str = "datasets/openstreetmap"
    SRTM_PATH: str = "datasets/srtm"

    SOLAR_MODEL_PATH: str = "models/solar_prediction_model.joblib"
    WIND_MODEL_PATH: str = "models/wind_prediction_model.joblib"
    SITE_MODEL_PATH: str = "models/site_suitability_model.joblib"

    REPORTS_OUTPUT_PATH: str = "reports/"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )


# Singleton settings instance — import this throughout the app
settings = Settings()
