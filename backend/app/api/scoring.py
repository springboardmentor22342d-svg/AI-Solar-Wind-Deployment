from fastapi import APIRouter, Request, Query
from app.scoring.site_scorer import calculate_site_score
from app.scoring.ranking import rank_sites

router = APIRouter()


@router.get("/scoring/site")
def score_single_site(
    request: Request,
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
):
    builder = request.app.state.feature_builder
    features = builder.build(latitude, longitude)
    return calculate_site_score(features)


@router.get("/scoring/rank-sample")
def rank_sample_sites(request: Request):
    """
    Demonstrates ranking using a small fixed set of Indian cities.
    A future version could accept a list of coordinates as input.
    """
    builder = request.app.state.feature_builder
    sample_coords = [
        {"name": "Bhopal", "lat": 23.2599, "lon": 77.4126},
        {"name": "Jodhpur", "lat": 26.2389, "lon": 73.0243},
        {"name": "Chennai", "lat": 13.0827, "lon": 80.2707},
    ]

    sites = []
    for coord in sample_coords:
        features = builder.build(coord["lat"], coord["lon"])
        features["name"] = coord["name"]
        sites.append(features)

    return rank_sites(sites)