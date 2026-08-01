import sys, os
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "backend"))

INPUT_CSV = "../datasets/processed/final_training_dataset.csv"
OUTPUT_CSV = "../datasets/processed/ml_training_data.csv"

FEATURE_COLUMNS = [
    "solar_irradiance", "elevation", "slope", "forest_pct", "net_area_sown_pct",
    "fallow_land_pct", "culturable_wasteland_pct",
    "distance_to_road_km", "distance_to_grid_km",
    "distance_to_nearest_settlement_km", "nearby_settlement_count",
    "temperature", "humidity",
]

MIN_GHI, MAX_GHI = 3.0, 7.0
MIN_CF, MAX_CF = 10.0, 22.0
REFERENCE_CAPACITY_KW = 5000
OPERATING_HOURS = 8760

def continuous_capacity_factor(ghi: float) -> float:
    clamped = max(MIN_GHI, min(MAX_GHI, ghi))
    return MIN_CF + (clamped - MIN_GHI) / (MAX_GHI - MIN_GHI) * (MAX_CF - MIN_CF)

if __name__ == "__main__":
    df = pd.read_csv(INPUT_CSV)

    before = len(df)
    df = df.dropna(subset=FEATURE_COLUMNS)
    after = len(df)
    print(f"Dropped {before - after} rows with missing values ({after} remaining)")

    df["capacity_factor_pct"] = df["solar_irradiance"].apply(continuous_capacity_factor)
    df["target_solar_energy_kwh_year"] = (
        REFERENCE_CAPACITY_KW * (df["capacity_factor_pct"] / 100) * OPERATING_HOURS
    ).round(2)

    final_df = df[FEATURE_COLUMNS + ["target_solar_energy_kwh_year"]]
    final_df.to_csv(OUTPUT_CSV, index=False)
    print(f"Saved {len(final_df)} rows, {len(FEATURE_COLUMNS)} features -> {OUTPUT_CSV}")
    print(final_df.head())
    print(f"Unique target values: {final_df['target_solar_energy_kwh_year'].nunique()} (should be close to {len(final_df)}, confirming no more collapsing)")