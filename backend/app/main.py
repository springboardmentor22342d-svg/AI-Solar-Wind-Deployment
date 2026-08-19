from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.home import router as home_router
from app.api.projects import router as projects_router
from app.api.sites import router as sites_router
from app.api.predictions import router as predictions_router

from app.database.database import engine, Base
from app.models.project import Project
from app.models.feature import Feature
from app.api.features import router as features_router
from app.api.evaluation import router as evaluation_router
from app.api.solar import router as solar_router
from app.api.analysis import router as analysis_router
from app.routers.forecast_router import router as forecast_router


app = FastAPI(
    title="Solar & Wind Deployment Intelligence Platform"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(home_router)
app.include_router(projects_router)
app.include_router(sites_router)
app.include_router(predictions_router)
app.include_router(features_router) 
app.include_router(evaluation_router)
app.include_router(solar_router)
app.include_router(analysis_router)
app.include_router(forecast_router)
