from app.feasibility.feasibility_engine import FeasibilityEngine

engine = FeasibilityEngine()

site = {
    "protected_area": True,
    "water_body": False,
    "slope": 18,
    "land_area": 3,
    "environmental_rating": 40,
    "distance_to_grid": 8,
    "distance_to_road": 6,
    "economic_rating": 55
}

result = engine.evaluate(site)

print(result)