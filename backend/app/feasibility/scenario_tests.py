from app.feasibility.feasibility_engine import FeasibilityEngine

engine = FeasibilityEngine()

feature = {
    "solar": 6,
    "wind": 7,
    "slope": 10,
    "road": 2,
    "grid": 3,
    "wind_capacity_factor": 0.55,
    "restricted_land": False
}
print(engine.evaluate(feature))