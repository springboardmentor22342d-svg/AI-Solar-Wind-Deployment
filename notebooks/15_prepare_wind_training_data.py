import pandas as pd

INPUT_CSV = "../datasets/processed/final_training_dataset.csv"
OUTPUT_CSV = "../datasets/processed/ml_wind_training_data.csv"

FEATURE_COLUMNS = [
    "wind_speed", "elevation", "slope", "forest_pct", "net_area_sown_pct",
    "fallow_land_pct", "culturable_wasteland_pct",
    "distance_to_road_km", "distance_to_grid_km",
    "distance_to_nearest_settlement_km", "nearby_settlement_count",
    "temperature", "humidity",
]

# Same continuous capacity factor approach as solar, adapted for wind
MIN_WS, MAX_WS = 2.0, 9.0
MIN_CF, MAX_CF = 10.0, 50.0
REFERENCE_CAPACITY_KW = 5000
OPERATING_HOURS = 8760

def continuous_wind_capacity_factor(wind_speed: float) -> float:
    clamped = max(MIN_WS, min(MAX_WS, wind_speed))
    return MIN_CF + (clamped - MIN_WS) / (MAX_WS - MIN_WS) * (MAX_CF - MIN_CF)

if __name__ == "__main__":
    df = pd.read_csv(INPUT_CSV)

    before = len(df)
    df = df.dropna(subset=FEATURE_COLUMNS)
    after = len(df)
    print(f"Dropped {before - after} rows with missing values ({after} remaining)")

    df["capacity_factor_pct"] = df["wind_speed"].apply(continuous_wind_capacity_factor)
    df["target_wind_energy_kwh_year"] = (
        REFERENCE_CAPACITY_KW * (df["capacity_factor_pct"] / 100) * OPERATING_HOURS
    ).round(2)

    final_df = df[FEATURE_COLUMNS + ["target_wind_energy_kwh_year"]]
    final_df.to_csv(OUTPUT_CSV, index=False)
    print(f"Saved {len(final_df)} rows -> {OUTPUT_CSV}")
    print(f"Unique target values: {final_df['target_wind_energy_kwh_year'].nunique()}")