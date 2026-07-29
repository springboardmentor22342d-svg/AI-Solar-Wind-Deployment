import pandas as pd
import rasterio
import json

def profile_csv(name, path):
    df = pd.read_csv(path)
    print(f"\n=== {name} ===")
    print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
    print(f"Column names & dtypes:\n{df.dtypes}")
    print(f"Missing values per column:\n{df.isna().sum()}")

def profile_tif(name, path):
    with rasterio.open(path) as src:
        print(f"\n=== {name} ===")
        print(f"Dimensions (rows x cols): {src.height} x {src.width}")
        print(f"Bands: {src.count}, Data type: {src.dtypes[0]}")
        print(f"CRS: {src.crs}")
        print(f"No-data value (missing marker): {src.nodata}")

def profile_geojson(name, path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    features = data["features"]
    print(f"\n=== {name} ===")
    print(f"Rows (features): {len(features)}")
    print(f"Property columns: {list(features[0]['properties'].keys())}")

# ---- Run for each raw dataset ----
profile_tif("Solar - GHI", "datasets/nasa_power/GHI.tif")
profile_tif("Solar - GTI", "datasets/nasa_power/GTI.tif")
profile_tif("Solar - OPTA", "datasets/nasa_power/OPTA.tif")
profile_tif("Wind Speed 100m", "datasets/global_wind_atlas/wind_speed_100m.tif")
profile_tif("Power Density 100m", "datasets/global_wind_atlas/power_density_100m.tif")
profile_csv("District Elevation", "datasets/srtm/Districts_elevation.csv")
profile_geojson("OSM Towns/Cities", "datasets/openstreetmap/osm-india-cities-towns.geojson")
profile_csv("State Land Use", "datasets/sentinel/states_land_use_pattern.csv")