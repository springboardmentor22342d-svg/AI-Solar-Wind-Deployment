"""
app/main.py – FastAPI Application Entrypoint.

This is the main application file that:
  1. Initializes the FastAPI app
  2. Sets up CORS (Cross-Origin Resource Sharing)
  3. Tests the database connection on startup
  4. Includes all the API routers from the app.api package

"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.config import settings
from app.database import test_db_connection, engine, Base
from app.models.project import Project
from app.api import (
    auth_router,
    solar_router,
    wind_router,
    site_router,
    sites_router,
    reports_router,
    projects_router,
    predictions_router,
    analysis_router,
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan events: Code to run before the app starts accepting requests,
    and code to run after it stops.
    """
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")

    # Test DB Connection and auto-create all tables on startup
    db_ok = test_db_connection()
    if not db_ok:
        logger.warning("Database is not reachable. App is starting, but DB endpoints will fail.")
    else:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables verified/created successfully.")
    
    yield  # App runs here
    
    logger.info("Shutting down application...")


# Initialize FastAPI Application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API for predicting solar/wind energy output and analyzing site suitability.",
    lifespan=lifespan,
)

# Configure CORS (Allows frontend on localhost:3000 to call backend on localhost:8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_prefix = settings.API_V1_STR

app.include_router(auth_router, prefix=f"{api_prefix}/auth", tags=["Authentication"])
app.include_router(solar_router, prefix=f"{api_prefix}/solar", tags=["Solar Prediction"])
app.include_router(wind_router, prefix=f"{api_prefix}/wind", tags=["Wind Prediction"])
app.include_router(site_router, prefix=f"{api_prefix}/site", tags=["Site Suitability Analysis"])
app.include_router(sites_router, prefix=f"{api_prefix}/sites", tags=["Sites"])
app.include_router(reports_router, prefix=f"{api_prefix}/reports", tags=["Report Generation"])
app.include_router(projects_router, prefix=f"{api_prefix}/projects", tags=["Projects"])
app.include_router(predictions_router, prefix=f"{api_prefix}/predictions", tags=["Predictions"])
app.include_router(analysis_router, prefix=f"{api_prefix}/analysis", tags=["Unified Analysis"])



@app.get("/", tags=["Health"])
def read_root():
    """Root endpoint – confirms API is online."""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "online",
        "docs": "/docs",
    }

@app.get("/ping", tags=["Health"])
def ping():
    """Simple liveness check."""
    return {"status": "ok", "service": "solar-wind-api"}

@app.get("/health", tags=["Health"])
def health():
    """Returns the current health status of the application."""
    return {"status": "running", "app": settings.APP_NAME}

@app.get("/db-health", tags=["Health"])
def db_health():
    """Returns the database connection status."""
    if test_db_connection():
        return {"status": "ok", "database": "connected"}
    raise HTTPException(status_code=503, detail="Database connection failed")

@app.get("/db-status", tags=["Health"])
def db_status():
    """Check database connection and return record counts for all tables."""
    from app.database import SessionLocal
    from sqlalchemy import text
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        tables = ["users", "projects", "solar_predictions", "wind_predictions", "site_analyses", "reports"]
        counts = {}
        for table in tables:
            try:
                result = db.execute(text(f"SELECT COUNT(*) FROM {table}"))
                counts[table] = result.scalar()
            except Exception:
                counts[table] = "error"
        return {"status": "connected", "table_counts": counts}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database connection failed: {str(e)}")
    finally:
        if 'db' in locals():
            db.close()
