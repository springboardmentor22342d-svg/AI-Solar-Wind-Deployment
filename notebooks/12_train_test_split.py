import pandas as pd
from sklearn.model_selection import train_test_split

INPUT_CSV = "../datasets/processed/ml_training_data.csv"

FEATURE_COLUMNS = [
    "solar_irradiance", "elevation", "slope", "forest_pct", "net_area_sown_pct",
    "fallow_land_pct", "culturable_wasteland_pct",
    "distance_to_road_km", "distance_to_grid_km",
    "distance_to_nearest_settlement_km", "nearby_settlement_count",
    "temperature", "humidity",
]
TARGET_COLUMN = "target_solar_energy_kwh_year"

if __name__ == "__main__":
    df = pd.read_csv(INPUT_CSV)
    X = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]

    # First split off the test set (10%)
    X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=0.10, random_state=42)

    # Then split remaining 90% into train (80% of total) and validation (10% of total)
    # 0.10 / 0.90 = 0.1111... to get exactly 10% of the ORIGINAL total as validation
    X_train, X_val, y_train, y_val = train_test_split(X_temp, y_temp, test_size=0.1111, random_state=42)

    print(f"Train: {len(X_train)} rows ({len(X_train)/len(df)*100:.1f}%)")
    print(f"Validation: {len(X_val)} rows ({len(X_val)/len(df)*100:.1f}%)")
    print(f"Test: {len(X_test)} rows ({len(X_test)/len(df)*100:.1f}%)")

    X_train.to_csv("../datasets/processed/X_train.csv", index=False)
    X_val.to_csv("../datasets/processed/X_val.csv", index=False)
    X_test.to_csv("../datasets/processed/X_test.csv", index=False)
    y_train.to_csv("../datasets/processed/y_train.csv", index=False)
    y_val.to_csv("../datasets/processed/y_val.csv", index=False)
    y_test.to_csv("../datasets/processed/y_test.csv", index=False)

    print("Saved all 6 split files to datasets/processed/")