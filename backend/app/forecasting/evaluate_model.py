import os

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split

from backend.app.forecasting.dataset_preparation import (
    DatasetPreparation
)

from backend.app.forecasting.model_evaluation import (
    ModelEvaluator,
    create_comparison_table
)


def main():

    # =================================================
    # 1. Load dataset
    # =================================================

    data_path = "datasets/nasa_power/solar_power_dataset.csv"

    df = pd.read_csv(data_path)

    print("Dataset loaded successfully.")
    print(f"Dataset shape: {df.shape}")

    print("\nDataset columns:")
    print(df.columns.tolist())

    # =================================================
    # 2. Prepare training dataset
    # =================================================

    dataset = DatasetPreparation(df)

    X, y = dataset.prepare_training_data()

    print("\nTraining dataset prepared.")
    print(f"Features shape: {X.shape}")
    print(f"Target shape: {y.shape}")

    print("\nFeatures used:")
    print(X.columns.tolist())

    # =================================================
    # 3. Split dataset
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

    print(f"Training samples   : {len(X_train)}")
    print(f"Validation samples : {len(X_validation)}")

    # =================================================
    # 4. Define models
    # =================================================

    models = {

        "Decision Tree": DecisionTreeRegressor(
            random_state=42
        ),

        "Random Forest": RandomForestRegressor(
            n_estimators=100,
            random_state=42
        )
    }

    # =================================================
    # 5. Train and evaluate each model
    # =================================================

    results = {}

    print("\n======================================")
    print("MODEL TRAINING AND EVALUATION")
    print("======================================")

    for name, model in models.items():

        print(f"\nTraining {name}...")

        # Train model
        model.fit(
            X_train,
            y_train
        )

        print(f"{name} training completed.")

        # Evaluate model
        results[name] = ModelEvaluator.evaluate_regression(
            model,
            X_train,
            y_train,
            X_validation,
            y_validation
        )

    # =================================================
    # 6. Create comparison table
    # =================================================

    comparison = create_comparison_table(
        results
    )

    print("\n======================================")
    print("MODEL COMPARISON TABLE")
    print("======================================")

    print(
        comparison.to_string(
            index=False
        )
    )

    # =================================================
    # 7. Display detailed results
    # =================================================

    print("\n======================================")
    print("DETAILED MODEL RESULTS")
    print("======================================")

    for model_name, result in results.items():

        print(f"\n{model_name}")

        print("Training:")
        print(
            f"  MAE  : "
            f"{result['train']['MAE']:.4f}"
        )

        print(
            f"  RMSE : "
            f"{result['train']['RMSE']:.4f}"
        )

        print(
            f"  R²   : "
            f"{result['train']['R2']:.4f}"
        )

        print(
            f"  MAPE : "
            f"{result['train']['MAPE']:.2f}%"
        )

        print("Validation:")

        print(
            f"  MAE  : "
            f"{result['validation']['MAE']:.4f}"
        )

        print(
            f"  RMSE : "
            f"{result['validation']['RMSE']:.4f}"
        )

        print(
            f"  R²   : "
            f"{result['validation']['R2']:.4f}"
        )

        print(
            f"  MAPE : "
            f"{result['validation']['MAPE']:.2f}%"
        )

    # =================================================
    # 8. Save comparison results
    # =================================================

    os.makedirs(
        "models",
        exist_ok=True
    )

    output_path = (
        "models/model_comparison.csv"
    )

    comparison.to_csv(
        output_path,
        index=False
    )

    print(
        f"\nComparison results saved to: "
        f"{output_path}"
    )


if __name__ == "__main__":
    main()