# Baseline Machine Learning Model - Performance Metrics

The first Machine Learning baseline for the Solar & Wind Deployment Intelligence Platform has been successfully trained. We utilized a **RandomForestRegressor** (from `scikit-learn`) to predict the `overall_score` (0-100) based on five engineered environmental and infrastructural features (Solar Irradiance, Wind Speed, Slope, Distance to Grid, and Distance to Road).

The model was trained on a synthetic dataset of 2,000 samples and evaluated on a 20% holdout test set (400 samples).

## Final Metrics

- **MAE (Mean Absolute Error):** 2.9091
- **RMSE (Root Mean Squared Error):** 3.5750
- **R² Score:** 0.8994

## What These Metrics Indicate

### 1. MAE (Mean Absolute Error)
**Result:** ~2.91 points.
**Meaning:** MAE measures the average absolute difference between the predicted overall score and the actual score. A value of 2.91 means that, on average, the model's predictions are off by only about 2.91 points on a 0-100 scale. This indicates very high accuracy for a baseline model and means the model's predictions are highly reliable for categorizing site suitability.

### 2. RMSE (Root Mean Squared Error)
**Result:** ~3.58 points.
**Meaning:** RMSE also measures the error but penalizes larger errors more heavily than smaller ones (because the errors are squared before averaging). The fact that RMSE (3.58) is very close to the MAE (2.91) implies that the model does not make massive, outlier mistakes. If the RMSE were much larger than the MAE, it would indicate that the model occasionally predicts wildly inaccurate scores. Here, the error is tightly clustered.

### 3. R² Score (Coefficient of Determination)
**Result:** ~0.899 (or 89.9%).
**Meaning:** The R² score represents the proportion of the variance in the target variable (`overall_score`) that is predictable from the input features. A score of 0.899 means that our Random Forest model explains roughly 90% of the variance in the site suitability scores. This is an exceptionally strong baseline result, indicating that the chosen environmental features are highly predictive of the final deployment suitability.

## Conclusion
The baseline model demonstrates robust predictive capabilities. The trained artifact (`baseline_rf_model.joblib`) has been persisted to the `models/` directory and is ready to be loaded by the FastAPI backend for real-time predictions in upcoming milestones.
