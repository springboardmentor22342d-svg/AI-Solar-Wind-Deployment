from fastapi import APIRouter, HTTPException

from app.services.geocoding_service import GeocodingService
from app.services.analysis_pipeline import AnalysisPipeline


router = APIRouter()

geocoder = GeocodingService()
pipeline = AnalysisPipeline()


@router.post("/analysis")
def analyze(
    village: str,
    district: str,
    state: str,
    country: str,
    date: str
):

    try:

        # 1. Convert location to coordinates
        location = geocoder.get_coordinates(
            village,
            district,
            state,
            country
        )

        latitude = location["latitude"]
        longitude = location["longitude"]

        # 2. Run your existing prediction pipeline

        result = pipeline.analyze(
            latitude,
            longitude,
            date)

        # 3. Add location information
        result["location"] = {
            "village": village,
            "district": district,
            "state": state,
            "country": country,
            "latitude": latitude,
            "longitude": longitude,
            "display_name": location["display_name"],
            "date": date
        }

        return result

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )