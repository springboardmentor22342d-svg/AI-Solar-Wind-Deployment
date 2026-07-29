import json
import random
import csv

TOWNS_GEOJSON = "datasets/openstreetmap/osm-india-cities-towns.geojson"
OUTPUT_CSV = "datasets/processed/candidate_sites.csv"

with open(TOWNS_GEOJSON, "r", encoding="utf-8") as f:
    towns_data = json.load(f)

# Keep only actual cities/towns (skip suburbs/other minor tags for cleaner candidates)
candidates = []
for feature in towns_data["features"]:
    props = feature["properties"]
    if props.get("place") not in ("city", "town"):
        continue
    lon, lat = feature["geometry"]["coordinates"]
    candidates.append({"name": props.get("name", "unknown"), "lat": lat, "lon": lon})

print(f"Total usable towns/cities found: {len(candidates)}")

# ---- Stratified sampling: divide India into a grid, sample a few per cell ----
# This guarantees geographic spread instead of random clustering in one region
GRID_SIZE_DEG = 2.0       # ~220km per cell
SAMPLES_PER_CELL = 16

grid = {}
for town in candidates:
    cell = (int(town["lat"] // GRID_SIZE_DEG), int(town["lon"] // GRID_SIZE_DEG))
    grid.setdefault(cell, []).append(town)

random.seed(42)  # fixed seed = same sample every time you re-run this
sampled_sites = []
for towns_in_cell in grid.values():
    sampled_sites.extend(random.sample(towns_in_cell, min(SAMPLES_PER_CELL, len(towns_in_cell))))

print(f"Sampled {len(sampled_sites)} sites across {len(grid)} regions of India")

with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "lat", "lon"])
    writer.writeheader()
    writer.writerows(sampled_sites)

print(f"Saved candidate site list to {OUTPUT_CSV}")