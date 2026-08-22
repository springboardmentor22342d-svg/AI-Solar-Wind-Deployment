import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
import joblib

X_train = pd.read_csv("../datasets/processed/X_train.csv")
X_val = pd.read_csv("../datasets/processed/X_val.csv")
y_train = pd.read_csv("../datasets/processed/y_train.csv").values.ravel()
y_val = pd.read_csv("../datasets/processed/y_val.csv").values.ravel()

if __name__ == "__main__":
    # Model 1: Decision Tree — deliberately simple baseline
    dt_model = DecisionTreeRegressor(random_state=42)
    dt_model.fit(X_train, y_train)
    print("Decision Tree trained.")

    # Model 2: Random Forest — ensemble of 100 trees
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    print("Random Forest trained.")

    # Quick sanity check: predict on a few validation rows
    print("\nSample predictions (Decision Tree):", dt_model.predict(X_val.head(3)))
    print("Sample predictions (Random Forest):", rf_model.predict(X_val.head(3)))
    print("Actual values:", y_val[:3])

    # Save both models temporarily (final "best model" save happens in Task 5)
    joblib.dump(dt_model, "../datasets/processed/decision_tree_model.pkl")
    joblib.dump(rf_model, "../datasets/processed/random_forest_model.pkl")
    print("\nBoth models saved temporarily for comparison.")