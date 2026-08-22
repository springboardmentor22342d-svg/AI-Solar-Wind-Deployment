"""
Prediction capabilities index — lists available ML prediction
endpoints and what each one does. Complements predict.py (which
performs the actual predictions) rather than duplicating it.
"""

from fastapi import APIRouter

router = APIRouter()

@router.get("/predictions")
def list_available_predictions():
    return {
        "available_predictions": [
            {
                "name": "Solar Energy Prediction",
                "endpoint": "/predict/solar",
                "method": "GET",
                "model": "Random Forest Regressor",
                "description": "Predicts annual solar energy output (kWh/year) for a given coordinate, based on 13 engineered environmental features.",
                "parameters": ["latitude", "longitude"],
            },
            {
                "name": "Wind Energy Prediction",
                "endpoint": "/predict/wind",
                "method": "GET",
                "model": "Random Forest Regressor",
                "description": "Predicts annual wind energy output (kWh/year) for a given coordinate, based on 13 engineered environmental features.",
                "parameters": ["latitude", "longitude"],
            },
            {
                "name": "Full Site Analysis",
                "endpoint": "/analysis",
                "method": "POST",
                "model": "Combined pipeline (ML + rule-based)",
                "description": "Runs the complete analysis workflow: environmental data, ML predictions, feasibility, energy yield, and financial metrics in one call. Requires authentication.",
                "parameters": ["latitude", "longitude", "project_name (optional)"],
            },
        ]
    }