import requests
import json
import os

# VK Maps high-capacity server
OVERPASS_URL = "https://maps.mail.ru/osm/tools/overpass/api/interpreter"

HEADERS = {
    "User-Agent": "SolarWindIntelligencePlatform/1.0"
}

# 1. Expressways & Trunks (Highest priority corridors)
MOTORWAY_TRUNK_QUERY = """
[out:json][timeout:300];
area["ISO3166-1"="IN"][admin_level=2]->.searchArea;
(
  way["highway"~"^(motorway|trunk)$"](area.searchArea);
);
out skel geom;
"""

# 2. Primary Highways
PRIMARY_QUERY = """
[out:json][timeout:300];
area["ISO3166-1"="IN"][admin_level=2]->.searchArea;
(
  way["highway"="primary"](area.searchArea);
);
out skel geom;
"""

# 3. Substations
SUBSTATIONS_QUERY = """
[out:json][timeout:300];
area["ISO3166-1"="IN"][admin_level=2]->.searchArea;
(
  node["power"="substation"](area.searchArea);
  way["power"="substation"](area.searchArea);
);
out center;
"""

def fetch_data(query: str, name: str) -> dict:
    print(f"Downloading {name}...")
    response = requests.post(OVERPASS_URL, data={"data": query}, headers=HEADERS, timeout=360)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Failed to fetch {name}. Status code: {response.status_code}")
        return None

if __name__ == "__main__":
    output_dir = "../datasets/openstreetmap"
    os.makedirs(output_dir, exist_ok=True)

    # Download roads in two lighter chunks and combine elements
    hw_data1 = fetch_data(MOTORWAY_TRUNK_QUERY, "Expressways and Trunks")
    hw_data2 = fetch_data(PRIMARY_QUERY, "Primary Roads")

    if hw_data1 and hw_data2:
        combined_elements = hw_data1.get("elements", []) + hw_data2.get("elements", [])
        hw_data1["elements"] = combined_elements
        
        roads_path = os.path.join(output_dir, "india_major_roads.json")
        with open(roads_path, "w", encoding="utf-8") as f:
            json.dump(hw_data1, f)
        print(f"✅ Saved India Major Roads -> {roads_path}")

    # Download substations
    sub_data = fetch_data(SUBSTATIONS_QUERY, "Substations")
    if sub_data:
        sub_path = os.path.join(output_dir, "india_substations.json")
        with open(sub_path, "w", encoding="utf-8") as f:
            json.dump(sub_data, f)
        print(f"✅ Saved India Substations -> {sub_path}")