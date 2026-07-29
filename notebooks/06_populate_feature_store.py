import sys
import os
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "backend"))

from app.database.database import SessionLocal
from app.services.feature_engineering.feature_builder import create_feature_builder
from app.services.feature_store_service import FeatureStoreService
from app.schemas.feature import FeatureCreate

CANDIDATE_SITES_CSV = "../datasets/processed/candidate_sites.csv"
BATCH_SIZE = 25

if __name__ == "__main__":
    sites_df = pd.read_csv(CANDIDATE_SITES_CSV)
    builder = create_feature_builder()
    db = SessionLocal()
    store = FeatureStoreService(db)

    total = len(sites_df)
    skipped = 0
    added = 0

    for i, site in sites_df.iterrows():
        lat, lon = site["lat"], site["lon"]

        # Cache lookup — skip if already computed (resumable, avoids
        # re-hitting the live NASA POWER climate API unnecessarily)
        existing = store.find_by_coordinates(lat, lon)
        if existing:
            skipped += 1
            continue

        raw = builder.build(lat, lon)

        feature_data = FeatureCreate(
            latitude=raw["latitude"],
            longitude=raw["longitude"],
            solar_irradiance=raw.get("solar_irradiance_ghi"),
            wind_speed=raw.get("wind_speed_100m"),
            temperature=raw.get("temperature"),
            humidity=raw.get("humidity"),
            elevation=raw.get("elevation"),
            slope=raw.get("slope"),
            solar_irradiance_gti=raw.get("solar_irradiance_gti"),
            optimum_tilt_angle=raw.get("optimum_tilt_angle"),
            power_density_100m=raw.get("power_density_100m"),
            nearby_settlement_count=raw.get("nearby_settlement_count"),
            distance_to_nearest_settlement_km=raw.get("distance_to_nearest_settlement_km"),
            nearest_settlement_name=raw.get("nearest_settlement_name"),
            distance_to_road_km=raw.get("distance_to_road_km"),
            distance_to_grid_km=raw.get("distance_to_grid_km"),
            forest_pct=raw.get("forest_pct"),
            net_area_sown_pct=raw.get("net_area_sown_pct"),
            fallow_land_pct=raw.get("fallow_land_pct"),
            culturable_wasteland_pct=raw.get("culturable_wasteland_pct"),
        )

        store.save(feature_data)
        added += 1

        if (i + 1) % BATCH_SIZE == 0:
            print(f"Progress: {i + 1}/{total} processed ({added} added, {skipped} skipped/cached)")

    db.close()
    print(f"Done. Total added: {added}, skipped (already cached): {skipped}, total in scope: {total}")