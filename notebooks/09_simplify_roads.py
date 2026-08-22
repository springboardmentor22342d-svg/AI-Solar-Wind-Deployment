import json
import csv

INPUT_FILE = "../datasets/openstreetmap/india_major_roads.json"
OUTPUT_FILE = "../datasets/openstreetmap/india_roads_simplified.csv"

if __name__ == "__main__":
    print("Loading roads file (this may take a minute, it's large)...")
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"Total road segments (ways): {len(data['elements'])}")

    points = []
    for element in data["elements"]:
        if element.get("type") != "way" or "geometry" not in element:
            continue
        # Keep every 5th point along each road, instead of every single
        # coordinate — drastically reduces size while still giving good
        # coverage for "nearest road" distance checks
        geometry = element["geometry"]
        for i in range(0, len(geometry), 5):
            points.append({"lat": geometry[i]["lat"], "lon": geometry[i]["lon"]})

    print(f"Simplified to {len(points)} sample points")

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["lat", "lon"])
        writer.writeheader()
        writer.writerows(points)

    print(f"Saved to {OUTPUT_FILE}")