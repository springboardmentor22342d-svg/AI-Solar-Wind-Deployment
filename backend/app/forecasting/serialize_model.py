


import os

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

from backend.app.forecasting.dataset_preparation import (
    DatasetPreparation
)


def main():

    # =================================================
    # 1. Load dataset
    # =================================================

    data_path = "datasets/nasa_power/solar_power_dataset.csv"

    df = pd.read_csv(data_path)

    print("Dataset loaded successfully.")
    print(f"Dataset shape: {df.shape}")

    # =================================================
    # 2. Prepare training data
    # =================================================

    dataset = DatasetPreparation(df)

    X, y = dataset.prepare_training_data()

    print("\nTraining dataset prepared.")
    print(f"Features shape: {X.shape}")
    print(f"Target shape: {y.shape}")

    # =================================================
    # 3. Split data
    # =================================================

    X_train, X_validation, y_train, y_validation = (
        train_test_split(
            X,
            y,
            test_size=0.2,
            shuffle=False,
            random_state=42
        )
    )

    print("\nDataset split completed.")
    print(f"Training samples: {len(X_train)}")
    print(f"Validation samples: {len(X_validation)}")

    # =================================================
    # 4. Create selected model
    # =================================================

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    # =================================================
    # 5. Train Random Forest
    # =================================================

    print("\nTraining Random Forest...")

    model.fit(
        X_train,
        y_train
    )

    print("Random Forest training completed.")

    # =================================================
    # 6. Create models directory
    # =================================================

    os.makedirs(
        "models",
        exist_ok=True
    )

    # =================================================
    # 7. Save trained model
    # =================================================

    model_path = "models/best_model.pkl"

    joblib.dump(
        model,
        model_path
    )

    print(
        f"\nModel saved successfully to: "
        f"{model_path}"
    )

    # =================================================
    # 8. Verify saved model
    # =================================================

    loaded_model = joblib.load(
        model_path
    )

    print(
        "\nSaved model loaded successfully."
    )

    print(
        f"Model type: "
        f"{type(loaded_model).__name__}"
    )

    # =================================================
    # 9. Test prediction
    # =================================================

    sample_prediction = loaded_model.predict(
        X_validation.iloc[:1]
    )

    print(
        f"Sample prediction: "
        f"{sample_prediction}"
    )


if __name__ == "__main__":
    main()