from fastapi import FastAPI
from app.api import (
    home, projects, sites, predictions, auth, features, evaluate,
    solar, deployment, scoring, energy, optimization, analysis, predict
)
from app.database.database import Base, engine
from app.models.project import Project
from app.models.site import Site
from app.models.user import User
from app.models.feature import Feature
from app.services.feature_engineering.feature_builder import create_feature_builder
from app.services.ml_prediction_service import MLPredictionService
from app.ml.feature_schema import SOLAR_MODEL_FEATURE_SCHEMA, WIND_MODEL_FEATURE_SCHEMA

app = FastAPI(title="Solar & Wind Deployment Intelligence Platform")

Base.metadata.create_all(bind=engine)

@app.on_event("startup")
def startup_event():
    app.state.feature_builder = create_feature_builder()
    app.state.solar_prediction_service = MLPredictionService(
        "solar_energy_model_final.pkl", SOLAR_MODEL_FEATURE_SCHEMA, "solar_irradiance"
    )
    app.state.wind_prediction_service = MLPredictionService(
        "wind_energy_model_final.pkl", WIND_MODEL_FEATURE_SCHEMA, "wind_speed"
    )

app.include_router(home.router)
app.include_router(projects.router)
app.include_router(sites.router)
app.include_router(predictions.router)
app.include_router(auth.router)
app.include_router(features.router)
app.include_router(evaluate.router)
app.include_router(solar.router)
app.include_router(deployment.router)
app.include_router(scoring.router)
app.include_router(energy.router)
app.include_router(optimization.router)
app.include_router(analysis.router)
app.include_router(predict.router)

@app.get("/health")
def health_check():
    return {"status": "Running"}

@app.get("/about")
def about():
    return {"project": "Solar & Wind Deployment Intelligence Platform"}