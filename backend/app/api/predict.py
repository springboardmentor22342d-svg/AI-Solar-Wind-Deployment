from fastapi import APIRouter, Request, Query

router = APIRouter()

@router.get("/predict/solar")
def predict_solar_energy(
    request: Request,
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
):
    builder = request.app.state.feature_builder
    features = builder.build(latitude, longitude)

    prediction_service = request.app.state.solar_prediction_service
    result = prediction_service.predict(features)

    return {
        "latitude": latitude,
        "longitude": longitude,
        **result,
    }

@router.get("/predict/wind")
def predict_wind_energy(
    request: Request,
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
):
    builder = request.app.state.feature_builder
    features = builder.build(latitude, longitude)

    # Alias wind_speed_100m -> wind_speed, matching the wind model's schema
    wind_features = {**features, "wind_speed": features.get("wind_speed_100m")}

    prediction_service = request.app.state.wind_prediction_service
    result = prediction_service.predict(wind_features)

    return {
        "latitude": latitude,
        "longitude": longitude,
        **result,
    }