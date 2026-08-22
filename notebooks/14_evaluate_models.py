import pandas as pd
import joblib
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

X_train = pd.read_csv("../datasets/processed/X_train.csv")
X_val = pd.read_csv("../datasets/processed/X_val.csv")
y_train = pd.read_csv("../datasets/processed/y_train.csv").values.ravel()
y_val = pd.read_csv("../datasets/processed/y_val.csv").values.ravel()

dt_model = joblib.load("../datasets/processed/decision_tree_model.pkl")
rf_model = joblib.load("../datasets/processed/random_forest_model.pkl")


def evaluate(model, X, y, set_name):
    predictions = model.predict(X)
    mae = mean_absolute_error(y, predictions)
    rmse = np.sqrt(mean_squared_error(y, predictions))
    r2 = r2_score(y, predictions)
    return {"set": set_name, "MAE": round(mae, 2), "RMSE": round(rmse, 2), "R2": round(r2, 4)}


if __name__ == "__main__":
    results = []

    results.append({"model": "Decision Tree", **evaluate(dt_model, X_train, y_train, "train")})
    results.append({"model": "Decision Tree", **evaluate(dt_model, X_val, y_val, "validation")})
    results.append({"model": "Random Forest", **evaluate(rf_model, X_train, y_train, "train")})
    results.append({"model": "Random Forest", **evaluate(rf_model, X_val, y_val, "validation")})

    results_df = pd.DataFrame(results)
    print(results_df.to_string(index=False))
    results_df.to_csv("../datasets/processed/model_comparison.csv", index=False)
    print("\nSaved comparison table to model_comparison.csv")


import joblib

rf_model = joblib.load("../datasets/processed/random_forest_model.pkl")
joblib.dump(rf_model, "../datasets/processed/solar_energy_model_final.pkl")
print("Final model saved as solar_energy_model_final.pkl")