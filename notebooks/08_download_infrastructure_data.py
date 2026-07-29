import requests
import json
import os

# High-reliability mirror suited for large spatial queries
OVERPASS_URL = "https://overpass.private.coffee/api/interpreter"

HEADERS = {
    "User-Agent": "SolarWindIntelligencePlatform/1.0"
}

# Major Roads Query for India (Motorway, Trunk, Primary)
ROADS_QUERY = """
[out:json][timeout:300];
area["ISO3166-1"="IN"][admin_level=2]->.searchArea;
(
  way["highway"~"^(motorway|trunk|primary)$"](area.searchArea);
);
out skel geom;
"""

# Power Substations Query for India
SUBSTATIONS_QUERY = """
[out:json][timeout:300];
area["ISO3166-1"="IN"][admin_level=2]->.searchArea;
(
  node["power"="substation"](area.searchArea);
  way["power"="substation"](area.searchArea);
);
out center;
"""

def download_dataset(query: str, output_path: str, dataset_name: str) -> None:
    print(f"Downloading India {dataset_name} (this may take 1-3 minutes)...")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    response = requests.post(
        OVERPASS_URL, 
        data={"data": query}, 
        headers=HEADERS, 
        timeout=360
    )
    
    if response.status_code == 200:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(response.json(), f)
        print(f"✅ Saved India {dataset_name} -> {output_path}")
    else:
        print(f"❌ Failed to download {dataset_name}. HTTP Status: {response.status_code}")
        print(response.text[:200])

if __name__ == "__main__":
    download_dataset(
        ROADS_QUERY, 
        "../datasets/openstreetmap/india_major_roads.json", 
        "Major Roads"
    )
    # download_dataset(
    #     SUBSTATIONS_QUERY, 
    #     "../datasets/openstreetmap/india_substations.json", 
    #     "Substations"
    # )