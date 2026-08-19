from app.feasibility.hard_constraints import HardConstraintValidator

validator = HardConstraintValidator()

site = {
    "protected_area": True,
    "water_body": False,
    "slope": 18,
    "land_area": 3,
    "environmental_rating": 40
}

print(validator.validate(site))