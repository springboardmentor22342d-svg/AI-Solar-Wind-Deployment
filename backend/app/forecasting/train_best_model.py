import pandas as pd
import joblib

from pathlib import Path
from sklearn.ensemble import RandomForestRegressor


DATASET_PATH = Path(
    "datasets/nasa_power/solar_power_dataset.csv"
)

MODEL_PATH = Path(
    "models/best_model.pkl"
)


def train_model():

    # Load dataset
    df = pd.read_csv(DATASET_PATH)

    # Convert date
    df["date"] = pd.to_datetime(df["date"])

    # Create time features
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["day"] = df["date"].dt.day
    df["day_of_year"] = df["date"].dt.dayofyear

    # EXACT features used by inference
    feature_columns = [
        "temperature",
        "humidity",
        "wind_speed",
        "solar_irradiance",
        "year",
        "month",
        "day",
        "day_of_year"
    ]

    # Target
    target_column = "total_yield"

    # Check columns
    missing = [
        column
        for column in feature_columns + [target_column]
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing columns: {missing}"
        )

    # Remove missing values
    df = df.dropna(
        subset=feature_columns + [target_column]
    )

    # Input and target
    X = df[feature_columns]
    y = df[target_column]

    # Train model
    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    model.fit(X, y)

    # Create models directory
    MODEL_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # Save model
    joblib.dump(
        model,
        MODEL_PATH
    )

    print("Model trained successfully.")
    print("Features used:")
    print(feature_columns)
    print(f"Model saved to: {MODEL_PATH}")


if __name__ == "__main__":
    train_model()