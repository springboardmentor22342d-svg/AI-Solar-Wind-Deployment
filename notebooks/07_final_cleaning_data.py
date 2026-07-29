import sys, os
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "backend"))
from app.database.database import SessionLocal
from app.models.feature import Feature

if __name__ == "__main__":
    db = SessionLocal()
    features = db.query(Feature).all()

    rows = [f.__dict__ for f in features]
    df = pd.DataFrame(rows).drop(columns=["_sa_instance_state"])

    before = len(df)
    df_clean = df.dropna(subset=["forest_pct", "wind_speed", "solar_irradiance", "elevation"])
    after = len(df_clean)

    df_clean.to_csv("../datasets/processed/final_training_dataset.csv", index=False)
    print(f"Exported {after} clean rows (excluded {before - after} border-region rows) to final_training_dataset.csv")

    db.close()