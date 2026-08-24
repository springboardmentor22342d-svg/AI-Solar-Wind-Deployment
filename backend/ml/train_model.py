import pandas as pd
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# ============================
# Load Dataset
# ============================

df = pd.read_csv("data/historical_data.csv")

# ============================
# Feature Engineering
# ============================

df["date"] = pd.to_datetime(df["date"])

df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month
df["day"] = df["date"].dt.day
df["day_of_year"] = df["date"].dt.dayofyear

# ============================
# Features and Target
# ============================

X = df[
    [
        "wind_speed",
        "temperature",
        "humidity",
        "year",
        "month",
        "day",
        "day_of_year"
    ]
]

y = df["solar_irradiance"]

# ============================
# Dataset Split
# 70% Train
# 15% Validation
# 15% Test
# ============================

X_train, X_temp, y_train, y_temp = train_test_split(
    X,
    y,
    test_size=0.30,
    random_state=42
)

X_val, X_test, y_val, y_test = train_test_split(
    X_temp,
    y_temp,
    test_size=0.50,
    random_state=42
)

print("Training Samples :", len(X_train))
print("Validation Samples :", len(X_val))
print("Testing Samples :", len(X_test))

# ============================
# Decision Tree Model
# ============================

dt_model = DecisionTreeRegressor(random_state=42)

dt_model.fit(X_train, y_train)

dt_train_pred = dt_model.predict(X_train)
dt_val_pred = dt_model.predict(X_val)

dt_train_mae = mean_absolute_error(y_train, dt_train_pred)
dt_val_mae = mean_absolute_error(y_val, dt_val_pred)

dt_train_rmse = mean_squared_error(
    y_train,
    dt_train_pred
) ** 0.5

dt_val_rmse = mean_squared_error(
    y_val,
    dt_val_pred
) ** 0.5

dt_train_r2 = r2_score(y_train, dt_train_pred)
dt_val_r2 = r2_score(y_val, dt_val_pred)

# ============================
# Random Forest Model
# ============================

rf_model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

rf_model.fit(X_train, y_train)

rf_train_pred = rf_model.predict(X_train)
rf_val_pred = rf_model.predict(X_val)

rf_train_mae = mean_absolute_error(y_train, rf_train_pred)
rf_val_mae = mean_absolute_error(y_val, rf_val_pred)

rf_train_rmse = mean_squared_error(
    y_train,
    rf_train_pred
) ** 0.5

rf_val_rmse = mean_squared_error(
    y_val,
    rf_val_pred
) ** 0.5

rf_train_r2 = r2_score(y_train, rf_train_pred)
rf_val_r2 = r2_score(y_val, rf_val_pred)

# ============================
# Print Comparison
# ============================

print("\n==============================")
print("Decision Tree Results")
print("==============================")

print("Train MAE :", dt_train_mae)
print("Validation MAE :", dt_val_mae)

print("Train RMSE :", dt_train_rmse)
print("Validation RMSE :", dt_val_rmse)

print("Train R2 :", dt_train_r2)
print("Validation R2 :", dt_val_r2)

print("\n==============================")
print("Random Forest Results")
print("==============================")

print("Train MAE :", rf_train_mae)
print("Validation MAE :", rf_val_mae)

print("Train RMSE :", rf_train_rmse)
print("Validation RMSE :", rf_val_rmse)

print("Train R2 :", rf_train_r2)
print("Validation R2 :", rf_val_r2)

# ============================
# Select Best Model
# ============================

if rf_val_rmse <= dt_val_rmse:
    best_model = rf_model
    best_name = "Random Forest"
else:
    best_model = dt_model
    best_name = "Decision Tree"

print("\nBest Model :", best_name)

# ============================
# Final Test Evaluation
# ============================

test_predictions = best_model.predict(X_test)

test_mae = mean_absolute_error(y_test, test_predictions)
test_rmse = mean_squared_error(
    y_test,
    test_predictions
) ** 0.5

test_r2 = r2_score(y_test, test_predictions)

print("\n==============================")
print("Best Model Test Performance")
print("==============================")

print("MAE :", test_mae)
print("RMSE :", test_rmse)
print("R2 Score :", test_r2)

# ============================
# Save Best Model
# ============================

os.makedirs("models", exist_ok=True)

joblib.dump(
    best_model,
    "models/random_forest_model.pkl"
)

print("\nBest model saved successfully!")
print("\n==========================")
print("Feature Importance")
print("============================")
feature_names = X.columns
importances = best_model.feature_importances_
importance_df = pd.DataFrame({
    "Feature": feature_names,
    "Importance": importances
})
importance_df = importance_df.sort_values(
    by="Importance",
    ascending=False
)
print(importance_df)
importance_df.to_csv(
    "models/feature_importance.csv",
    index=False
)