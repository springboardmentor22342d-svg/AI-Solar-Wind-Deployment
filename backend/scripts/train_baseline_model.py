import os
import sys
import json
import numpy as np
import pandas as pd
import joblib
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.evaluation.scorer import compute_weighted_score

def generate_synthetic_dataset(num_samples=2000):
    print(f"Generating synthetic dataset with {num_samples} samples...")
    np.random.seed(42)
    
    solar_irradiance = np.random.uniform(2.0, 8.0, num_samples)
    wind_speed = np.random.uniform(1.0, 12.0, num_samples)
    slope = np.random.uniform(0.0, 25.0, num_samples)
    dist_grid = np.random.uniform(0.1, 50.0, num_samples)
    dist_road = np.random.uniform(0.1, 20.0, num_samples)
    
    features_list = []
    targets = []
    
    for i in range(num_samples):
        features = {
            "solar_irradiance_kwh": solar_irradiance[i],
            "wind_speed_ms": wind_speed[i],
            "slope_deg": slope[i],
            "dist_grid_km": dist_grid[i],
            "dist_road_km": dist_road[i],
        }
        
        base_score = compute_weighted_score(features)
        noise = np.random.normal(0, 3.0) 
        noisy_score = np.clip(base_score + noise, 0.0, 100.0)
        
        features_list.append(features)
        targets.append(noisy_score)
        
    df = pd.DataFrame(features_list)
    df['overall_score'] = targets
    return df

def evaluate_model(model, X, y):
    y_pred = model.predict(X)
    return {
        "MAE": mean_absolute_error(y, y_pred),
        "RMSE": np.sqrt(mean_squared_error(y, y_pred)),
        "R2": r2_score(y, y_pred)
    }

def train_and_evaluate():
    # 1. Prepare Dataset and Split (70/15/15)
    df = generate_synthetic_dataset()
    
    X = df[["solar_irradiance_kwh", "wind_speed_ms", "slope_deg", "dist_grid_km", "dist_road_km"]]
    y = df["overall_score"]
    
    # Split 1: Train (70%), Temp (30%)
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42)
    # Split 2: Val (15%), Test (15%) from Temp
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)
    
    print(f"Data Split -> Train: {len(X_train)}, Val: {len(X_val)}, Test: {len(X_test)}")
    
    # 2. Train Two Baseline Models
    print("\nTraining Decision Tree Regressor...")
    dt_model = DecisionTreeRegressor(random_state=42) # Prone to overfitting without max_depth
    dt_model.fit(X_train, y_train)
    
    print("Training Random Forest Regressor...")
    rf_model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
    rf_model.fit(X_train, y_train)
    
    # 3. Compare Model Performance (Train vs Val)
    results = {
        "DecisionTree": {
            "Train": evaluate_model(dt_model, X_train, y_train),
            "Val": evaluate_model(dt_model, X_val, y_val)
        },
        "RandomForest": {
            "Train": evaluate_model(rf_model, X_train, y_train),
            "Val": evaluate_model(rf_model, X_val, y_val)
        }
    }
    
    # Determine the best model based on Validation RMSE
    best_model_name = "RandomForest" if results["RandomForest"]["Val"]["RMSE"] < results["DecisionTree"]["Val"]["RMSE"] else "DecisionTree"
    best_model = rf_model if best_model_name == "RandomForest" else dt_model
    
    print(f"\nBest Model Selected: {best_model_name}")
    
    # Evaluate best model on Test set
    test_metrics = evaluate_model(best_model, X_test, y_test)
    results[best_model_name]["Test"] = test_metrics
    
    # Save results to json for reporting
    models_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
    os.makedirs(models_dir, exist_ok=True)
    with open(os.path.join(models_dir, 'model_comparison_results.json'), 'w') as f:
        json.dump(results, f, indent=4)
        
    # 4. Save best model
    model_path = os.path.join(models_dir, 'best_baseline_model.joblib')
    joblib.dump(best_model, model_path)
    print(f"Saved {best_model_name} to {model_path}")

if __name__ == "__main__":
    train_and_evaluate()
