from app.api.auth import router as auth_router
from app.api.solar import router as solar_router
from app.api.wind import router as wind_router
from app.api.site import router as site_router
from app.api.sites import router as sites_router
from app.api.reports import router as reports_router
from app.api.projects import router as projects_router
from app.api.home import router as home_router
from app.api.predictions import router as predictions_router
from app.api.analysis import router as analysis_router

__all__ = [
    "auth_router",
    "solar_router",
    "wind_router",
    "site_router",
    "sites_router",
    "reports_router",
    "projects_router",
    "home_router",
    "predictions_router",
    "analysis_router",
]
