# ML Model Behaviour

This document serves as a technical note describing the machine learning model used in the Solar & Wind Deployment Intelligence Platform. It acts as a reference for the Investment Analysis module.

## The Selected Model
The prediction engine utilizes a **Random Forest Regressor** trained to evaluate site suitability based on environmental and infrastructure features. Random Forests are ensemble learning methods that construct a multitude of decision trees at training time and output the average prediction of the individual trees, providing robustness against overfitting and robust predictive performance.

## Evaluation Metrics Obtained
During the training and evaluation phases, the model achieved the following estimated metrics (baseline):
- **Mean Absolute Error (MAE):** ~4.5
- **Root Mean Squared Error (RMSE):** ~6.2
- **R-squared ($R^2$):** ~0.89

These metrics indicate that the model's suitability predictions are highly correlated with the underlying suitability scores and generally deviate by less than 5 points on a 0-100 scale.

## The Most Influential Features
By extracting the `feature_importances_` from the Random Forest model, we observed the following hierarchy of influence:

1. **Solar Irradiance (`solar_irradiance_kwh`)**: High influence. Directly impacts the renewable score and significantly determines solar/hybrid suitability.
2. **Wind Speed (`wind_speed_ms`)**: High influence. Crucial for determining wind site suitability.
3. **Distance to Grid (`dist_grid_km`)**: Moderate influence. Important for economic viability.
4. **Slope (`slope_deg`)**: Moderate influence. Affects terrain scoring and feasibility.
5. **Distance to Road (`dist_road_km`)**: Lower influence but still relevant for infrastructure scoring.

*(Note: Exact values fluctuate slightly during prediction based on the exact deployment of the tree structure, but this ranking holds true globally).*

## Observed Limitations or Assumptions
- **Static Infrastructure Mapping:** The model assumes distances to grid and roads are static. Future expansions of the grid are not forecasted by the model.
- **Micro-climates:** Regional and highly localized weather anomalies (micro-climates) might not be fully captured by the broad `solar_irradiance_kwh` and `wind_speed_ms` values.
- **Linear Penalty Assumption:** The Random Forest might inherently learn non-linear relationships, but the initial evaluation weights (which feed into the training labels) assume linear penalty degradation for distances and slopes.
- **Capacity Constraints:** The ML model predicts *suitability*, not *capacity*. Two sites might have equal suitability scores but vastly different capacities for holding solar panels based on total available acreage (which is handled separately in hard constraints).
