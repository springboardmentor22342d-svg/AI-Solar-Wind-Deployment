import sys
import os
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "backend"))

from app.services.feature_engineering.feature_builder import create_feature_builder
from app.services.feature_engineering.energy_formulas import (
    estimate_solar_energy_kwh_per_year,
    estimate_wind_energy_kwh_per_year,
)

CANDIDATE_SITES_CSV = "datasets/processed/candidate_sites.csv"
OUTPUT_CSV = "datasets/processed/training_dataset.csv"

if __name__ == "__main__":
    sites_df = pd.read_csv(CANDIDATE_SITES_CSV)
    builder = create_feature_builder()

    rows = []
    total = len(sites_df)
    print(f"Building training dataset for {total} candidate sites...", flush=True)

    for i, site in sites_df.iterrows():
        lat, lon = site["lat"], site["lon"]
        features = builder.build(lat, lon)
        features["name"] = site["name"]

        features["target_solar_energy_kwh_year"] = estimate_solar_energy_kwh_per_year(
            features.get("solar_irradiance_ghi")
        )
        features["target_wind_energy_kwh_year"] = estimate_wind_energy_kwh_per_year(
            features.get("wind_speed_100m"), features.get("elevation")
        )

        rows.append(features)

        if (i + 1) % 25 == 0 or (i + 1) == total:
            print(f"Processed {i + 1}/{total} sites...", flush=True)

    training_df = pd.DataFrame(rows)

    before = len(training_df)
    training_df = training_df.dropna(subset=[
        "solar_irradiance_ghi", "wind_speed_100m", "elevation",
        "forest_pct",
        "target_solar_energy_kwh_year", "target_wind_energy_kwh_year"
    ])
    after = len(training_df)

    training_df.to_csv(OUTPUT_CSV, index=False)
    print(f"Saved {after} clean training rows to {OUTPUT_CSV} (dropped {before - after} incomplete rows)")
