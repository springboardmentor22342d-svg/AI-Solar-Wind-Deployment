import pandas as pd
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "backend"))

from app.database.database import SessionLocal
from app.models.site import Site

df = pd.read_csv("datasets/processed/site_features.csv")

db = SessionLocal()

for _, row in df.iterrows():
    site = Site(
        name=row["name"],
        latitude=row["lat"],
        longitude=row["lon"],
        ghi=row["GHI"],
        gti=row["GTI"],
        opta=row["OPTA"],
        wind_speed_100m=row["wind_speed_100m"],
        power_density_100m=row["power_density_100m"],
        elevation=row["elevation"],
        nearby_settlement_count=row["nearby_settlement_count"],
        distance_to_nearest_settlement_km=row["distance_to_nearest_settlement_km"],
        nearest_settlement_name=row["nearest_settlement_name"],
        forest_pct=row["forest_pct"],
        net_area_sown_pct=row["net_area_sown_pct"],
        fallow_land_pct=row["fallow_land_pct"],
        culturable_wasteland_pct=row["culturable_wasteland_pct"],
    )
    db.add(site)

db.commit()
db.close()
print(f"Imported {len(df)} sites into the database.")