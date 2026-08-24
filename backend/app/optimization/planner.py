from .strategy import recommend_strategy
from .capacity import recommend_capacity
from .expansion import expansion_status

def generate_plan(site):
    technology = recommend_strategy(site)
    capacity = recommend_capacity(site)
    expansion = expansion_status(site)
    if technology == "Hybrid":
        remarks = "Excellent renewable resource availability."
    elif technology == "Solar":
        remarks = "Solar resources are stronger than wind."
    else:
        remarks = "Wind resources are stronger than solar."
    return {
        "recommended_technology": technology,
        "recommended_capacity": capacity,
        "expansion_status": expansion,
        "optimization_remarks": remarks
    }