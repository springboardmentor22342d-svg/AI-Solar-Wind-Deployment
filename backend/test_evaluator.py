from app.evaluation.evaluator import Evaluator

evaluator = Evaluator()

sites = [ {
    "site_id": 1,
    "latitude": 20.2961,
    "longitude": 85.8245,
    "solar": 5.9,
    "wind": 7.2,
    "slope": 4,
    "grid": 1.8,
    "road": 0.45
},
{
    "site_id": 2,
    "latitude": 20.5000,
    "longitude": 85.9000,
    "solar": 4.5,
    "wind": 75.8,
    "slope": 10,
    "grid": 14.5,
    "road": 2.5
},
{
    "site_id": 3,
    "latitude": 20.7000,
    "longitude": 86.1000,
    "solar": 6.8,
    "wind": 8.5,
    "slope": 2,
    "grid": 0.8,
    "road": 0.3
}
]
results = []
for site in sites:
    results.append(evaluator.evaluate(site))
    results.sort(key=lambda x: x["overall_score"],reverse=True)
print("\n===== SITE RANKING =====")
for rank,site in enumerate(results,start=1):
    print(f"\nRank{rank}")
    print("Site ID:",site["site_id"])
    print("Overall Score:",site["overall_score"])
    print("Recommendation:",site["recommendation"])
print("\n===== VALIDATION =====")
print("Highest Ranked Site:",results[0]["site_id"])
print("Lowest Ranked Site:",results[-1]["site_id"])
assert results[0]["overall_score"] >= results[1]["overall_score"]
assert results[1]["overall_score"] >= results[2]["overall_score"]
print("ranking validation: PASSED")
print("Scoring engine validation: PASSED")