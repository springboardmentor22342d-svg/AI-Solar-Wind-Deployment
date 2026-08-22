import rasterio
import pandas as pd
import json
import math
import reverse_geocoder as rg

# ============ CONFIG ============
SOLAR_DIR = "datasets/nasa_power/"
WIND_SPEED_TIF = "datasets/global_wind_atlas/wind_speed_100m.tif"
POWER_DENSITY_TIF = "datasets/global_wind_atlas/power_density_100m.tif"
ELEVATION_CSV = "datasets/srtm/Districts_elevation.csv"
TOWNS_GEOJSON = "datasets/openstreetmap/osm-india-cities-towns.geojson"
LANDUSE_CSV = "datasets/sentinel/states_land_use_pattern.csv"
SITES_CSV = "datasets/processed/candidate_sites.csv"
OUTPUT_CSV = "datasets/processed/site_features.csv"

# ============ LOAD REFERENCE DATA ============
elevation_df = pd.read_csv(ELEVATION_CSV)
landuse_df = pd.read_csv(LANDUSE_CSV)

with open(TOWNS_GEOJSON, "r", encoding="utf-8") as f:
    towns_data = json.load(f)

towns = []
for feature in towns_data["features"]:
    props = feature["properties"]
    lon, lat = feature["geometry"]["coordinates"]
    towns.append({"name": props.get("name", "unknown"), "lat": lat, "lon": lon})

sites_df = pd.read_csv(SITES_CSV)
SITES = sites_df.to_dict("records")

# ============ 1. SOLAR (memory-safe point sampling) ============
def get_solar_values(lat, lon):
    values = {}
    for param in ["GHI", "GTI", "OPTA"]:
        path = f"{SOLAR_DIR}{param}.tif"
        with rasterio.open(path) as src:
            value = next(src.sample([(lon, lat)]))[0]
            values[param] = float(value)
    return values

# ============ 2. WIND (memory-safe point sampling) ============
def get_wind_from_atlas(lat, lon):
    values = {}
    for name, path in [
        ("wind_speed_100m", WIND_SPEED_TIF),
        ("power_density_100m", POWER_DENSITY_TIF),
    ]:
        with rasterio.open(path) as src:
            value = next(src.sample([(lon, lat)]))[0]
            values[name] = float(value)
    return values

# ============ 3. ELEVATION ============
def get_elevation(lat, lon):
    dist = ((elevation_df["Latitude"] - lat) ** 2 + (elevation_df["Longitude"] - lon) ** 2) ** 0.5
    nearest = elevation_df.loc[dist.idxmin()]
    return float(nearest["elevation"])

# ============ 4. INFRASTRUCTURE ============
def get_infrastructure_score(lat, lon, radius_km=30):
    km_per_deg_lat = 111.0
    km_per_deg_lon = 111.0 * math.cos(math.radians(lat))
    avg_km_per_deg = (km_per_deg_lat + km_per_deg_lon) / 2

    nearby_count = 0
    min_dist_km = float("inf")
    nearest_name = None

    for town in towns:
        dist_deg = ((town["lat"] - lat) ** 2 + (town["lon"] - lon) ** 2) ** 0.5
        dist_km = dist_deg * avg_km_per_deg
        if dist_km < min_dist_km:
            min_dist_km = dist_km
            nearest_name = town["name"]
        if dist_km <= radius_km:
            nearby_count += 1

    return {
        "nearby_settlement_count": nearby_count,
        "distance_to_nearest_settlement_km": round(min_dist_km, 2),
        "nearest_settlement_name": nearest_name,
    }

# ============ 5. LAND COVER ============
def get_land_cover(state_name):
    match = landuse_df[
        (landuse_df["States/UTs"].str.lower() == state_name.lower()) &
        (landuse_df["Category"] == "Percentage to Geographical Area")
    ]
    if not match.empty:
        row = match.iloc[0]
        return {
            "forest_pct": row["Forests"],
            "net_area_sown_pct": row["Net area sown"],
            "fallow_land_pct": row["Current fallows"],
            "culturable_wasteland_pct": row["Culturable wasteland"],
        }
    return {
        "forest_pct": None,
        "net_area_sown_pct": None,
        "fallow_land_pct": None,
        "culturable_wasteland_pct": None,
    }

# ============ MAIN ============
STATE_NAME_FIXES = {
    "Maharashtra": "Mahrashtra",
    "Telangana": "Andhra Pradesh",   # your CSV pre-dates the 2014 state split
    "Andaman and Nicobar Islands": "Andaman & Nicobar Islands",  # "and" vs "&"
    "Laccadives": "Lakshwadeep",     # older name for Lakshadweep
}

def get_land_cover(state_name):
    state_name = STATE_NAME_FIXES.get(state_name, state_name)  # correct known typos first
    match = landuse_df[
        (landuse_df["States/UTs"].str.lower() == state_name.lower()) &
        (landuse_df["Category"] == "Percentage to Geographical Area")
    ]
    if not match.empty:
        row = match.iloc[0]
        return {
            "forest_pct": row["Forests"],
            "net_area_sown_pct": row["Net area sown"],
            "fallow_land_pct": row["Current fallows"],
            "culturable_wasteland_pct": row["Culturable wasteland"],
        }
    return {
        "forest_pct": None,
        "net_area_sown_pct": None,
        "fallow_land_pct": None,
        "culturable_wasteland_pct": None,
    }



if __name__ == "__main__":
    # Batch geocode ALL sites in one call — avoids repeated multiprocessing spawns
    coords_list = [(site["lat"], site["lon"]) for site in SITES]
    geocode_results = rg.search(coords_list)


    rows = []
    for i, site in enumerate(SITES):
        lat, lon = site["lat"], site["lon"]
        row = {"name": site["name"], "lat": lat, "lon": lon}
        row.update(get_solar_values(lat, lon))
        row.update(get_wind_from_atlas(lat, lon))
        row["elevation"] = get_elevation(lat, lon)
        row.update(get_infrastructure_score(lat, lon))
        state_name = geocode_results[i]["admin1"]
        row.update(get_land_cover(state_name))
        rows.append(row)

    final_df = pd.DataFrame(rows)
    final_df.to_csv(OUTPUT_CSV, index=False)
    print(final_df.shape)
    print(final_df.head())

    final_df = final_df.dropna(subset=["wind_speed_100m", "forest_pct"])
    print(f"Final dataset: {final_df.shape[0]} sites (dropped border-region rows with incomplete coverage)")

