import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "backend"))

import joblib
import pandas as pd
from app.ml.feature_schema import SOLAR_MODEL_FEATURE_SCHEMA, WIND_MODEL_FEATURE_SCHEMA

SOLAR_MODEL_PATH = "../models/solar_energy_model_final.pkl"
WIND_MODEL_PATH = "../models/wind_energy_model_final.pkl"


def get_feature_importance(model_path: str, schema: list, model_name: str) -> pd.DataFrame:
    model = joblib.load(model_path)
    importance_df = pd.DataFrame({
        "feature": schema,
        "importance": model.feature_importances_,
    }).sort_values("importance", ascending=False).reset_index(drop=True)
    importance_df["model"] = model_name
    return importance_df


if __name__ == "__main__":
    solar_importance = get_feature_importance(SOLAR_MODEL_PATH, SOLAR_MODEL_FEATURE_SCHEMA, "Solar")
    wind_importance = get_feature_importance(WIND_MODEL_PATH, WIND_MODEL_FEATURE_SCHEMA, "Wind")

    print("=== Solar Model Feature Importance ===")
    print(solar_importance.to_string(index=False))

    print("\n=== Wind Model Feature Importance ===")
    print(wind_importance.to_string(index=False))

    combined = pd.concat([solar_importance, wind_importance])
    combined.to_csv("../datasets/processed/feature_importance.csv", index=False)
    print("\nSaved to feature_importance.csv")