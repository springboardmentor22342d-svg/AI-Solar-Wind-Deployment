import pandas as pd
import numpy as np
import joblib
import time
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

X_train = pd.read_csv("../datasets/processed/X_train_wind.csv")
X_val = pd.read_csv("../datasets/processed/X_val_wind.csv")
y_train = pd.read_csv("../datasets/processed/y_train_wind.csv").values.ravel()
y_val = pd.read_csv("../datasets/processed/y_val_wind.csv").values.ravel()


def evaluate(model, X, y, set_name):
    predictions = model.predict(X)
    return {
        "set": set_name,
        "MAE": round(mean_absolute_error(y, predictions), 2),
        "RMSE": round(np.sqrt(mean_squared_error(y, predictions)), 2),
        "R2": round(r2_score(y, predictions), 4),
    }


if __name__ == "__main__":
    results = []

    start = time.time()
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    rf_train_time = round(time.time() - start, 3)

    start = time.time()
    xgb_model = XGBRegressor(n_estimators=100, random_state=42)
    xgb_model.fit(X_train, y_train)
    xgb_train_time = round(time.time() - start, 3)

    results.append({"model": "Random Forest", "train_time_sec": rf_train_time, **evaluate(rf_model, X_train, y_train, "train")})
    results.append({"model": "Random Forest", "train_time_sec": rf_train_time, **evaluate(rf_model, X_val, y_val, "validation")})
    results.append({"model": "XGBoost", "train_time_sec": xgb_train_time, **evaluate(xgb_model, X_train, y_train, "train")})
    results.append({"model": "XGBoost", "train_time_sec": xgb_train_time, **evaluate(xgb_model, X_val, y_val, "validation")})

    results_df = pd.DataFrame(results)
    print(results_df.to_string(index=False))
    results_df.to_csv("../datasets/processed/wind_model_comparison.csv", index=False)

    joblib.dump(rf_model, "../datasets/processed/wind_random_forest_model.pkl")
    joblib.dump(xgb_model, "../datasets/processed/wind_xgboost_model.pkl")
    print("\nBoth models saved for comparison.")

import joblib
wind_rf_model = joblib.load("../datasets/processed/wind_random_forest_model.pkl")
joblib.dump(wind_rf_model, "../datasets/processed/wind_energy_model_final.pkl")
print("Final wind model saved")