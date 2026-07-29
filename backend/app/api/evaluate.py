from fastapi import APIRouter, Request, Query
from app.evaluation.evaluator import evaluate_site

router = APIRouter()

@router.get("/evaluate")
def evaluate_location(
    request: Request,
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
):
    """
    Full live pipeline: coordinate in -> FeatureBuilder computes
    features -> evaluator scores and recommends -> combined result out.
    """
    builder = request.app.state.feature_builder
    features = builder.build(latitude, longitude)

    # Map FeatureBuilder's output keys to the evaluator's expected keys
    evaluation_input = {
    "solar_irradiance": features.get("solar_irradiance"),
    "wind_speed": features.get("wind_speed_100m"),
    "slope": features.get("slope"),
    "distance_to_grid_km": features.get("distance_to_grid_km"),
    "distance_to_road_km": features.get("distance_to_road_km"),
    "forest_pct": features.get("forest_pct"),
    "culturable_wasteland_pct": features.get("culturable_wasteland_pct"),
}

    result = evaluate_site(evaluation_input)
    result["latitude"] = latitude
    result["longitude"] = longitude
    result["raw_features"] = features

    return result