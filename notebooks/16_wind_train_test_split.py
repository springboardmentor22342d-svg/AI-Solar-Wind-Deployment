import pandas as pd
from sklearn.model_selection import train_test_split

INPUT_CSV = "../datasets/processed/ml_wind_training_data.csv"

FEATURE_COLUMNS = [
    "wind_speed", "elevation", "slope", "forest_pct", "net_area_sown_pct",
    "fallow_land_pct", "culturable_wasteland_pct",
    "distance_to_road_km", "distance_to_grid_km",
    "distance_to_nearest_settlement_km", "nearby_settlement_count",
    "temperature", "humidity",
]
TARGET_COLUMN = "target_wind_energy_kwh_year"

if __name__ == "__main__":
    df = pd.read_csv(INPUT_CSV)
    X = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]

    X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=0.10, random_state=42)
    X_train, X_val, y_train, y_val = train_test_split(X_temp, y_temp, test_size=0.1111, random_state=42)

    print(f"Train: {len(X_train)}, Validation: {len(X_val)}, Test: {len(X_test)}")

    X_train.to_csv("../datasets/processed/X_train_wind.csv", index=False)
    X_val.to_csv("../datasets/processed/X_val_wind.csv", index=False)
    X_test.to_csv("../datasets/processed/X_test_wind.csv", index=False)
    y_train.to_csv("../datasets/processed/y_train_wind.csv", index=False)
    y_val.to_csv("../datasets/processed/y_val_wind.csv", index=False)
    y_test.to_csv("../datasets/processed/y_test_wind.csv", index=False)
    print("Saved wind split files.")