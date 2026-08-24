from app.optimization import OptimizationEngine

engine = OptimizationEngine()

sites = [
    {
        "name": "Solar Site",
        "solar_capacity_factor": 0.24,
        "wind_capacity_factor": 0.18,
        "land_area": 60
    },
    {
        "name": "Wind Site",
        "solar_capacity_factor": 0.18,
        "wind_capacity_factor": 0.42,
        "land_area": 120
    },
    {
        "name": "Hybrid Site",
        "solar_capacity_factor": 0.23,
        "wind_capacity_factor": 0.37,
        "land_area": 150
    }
]
results = []
for site in sites:
    print("\n======================")
    print(site["name"])

    result = engine.optimize(site)
    print(result)

    results.append(result)
print("\n===== VALIDATION =====")

assert results[0]["recommended_technology"] == "Solar"
assert results[1]["recommended_technology"] == "Wind"
assert results[2]["recommended_technology"] == "Hybrid"

print("Technology selection: PASSED")

assert results[1]["recommended_capacity"] > results[0]["recommended_capacity"]
print("Capacity planning: PASSED")

assert results[2]["expansion_status"] == "Expandable"
print("Expansion analysis: PASSED")

print("Optimization Engine validation: PASSED")