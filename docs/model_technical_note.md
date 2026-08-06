# Technical Note: Prediction Models

## Selected Models

| Target | Model | Alternative Compared | Selection Reason |
|---|---|---|---|
| Solar energy (kWh/year) | Random Forest | Decision Tree | Decision Tree showed textbook overfitting (train R²=1.0000, zero training error); Random Forest showed realistic, consistent train/validation performance |
| Wind energy (kWh/year) | Random Forest | XGBoost | XGBoost's train/validation error gap was ~16x wider (untuned overfitting); Random Forest generalized more reliably despite slightly longer training time |

## Evaluation Metrics

| Model | Train MAE | Val MAE | Train R² | Val R² |
|---|---|---|---|---|
| Solar (Random Forest) | 1,276.63 | 1,886.47 | 0.9996 | 0.9998 |
| Wind (Random Forest) | 3,860.09 | 9,680.65 | 1.0000 | 0.9999 |

## Most Influential Features

- **Solar model:** `solar_irradiance` (99.82% importance) — overwhelmingly dominant, consistent with solar energy physics.
- **Wind model:** `wind_speed` (99.98% importance) — overwhelmingly dominant, consistent with the cubic relationship between wind speed and power.
- All secondary features (elevation, slope, land-use, infrastructure distances) individually contribute less than 0.1% importance in both models.

## Observed Limitations and Assumptions

1. **Target construction limits secondary feature signal.** Training targets were computed using a continuous capacity-factor formula that is a direct mathematical function of irradiance (solar) or wind speed (wind) alone. As a result, no other engineered feature was ever mathematically linked to the target during data generation, so near-zero importance for those features is an expected consequence of target design, not a data quality or feature engineering failure. Real-world energy yield is influenced by additional factors (terrain, shading, transmission losses); capturing this would require either genuine measured production data or a more sophisticated multi-factor target formula.

2. **Reference capacity assumption.** All predictions are generated for a fixed 5,000 kW reference installation. Actual predictions scale linearly with installed capacity but are not currently parameterized by capacity as a model input.

3. **Missing-data handling.** Approximately 10 sites (out of 1,310) were excluded from training due to missing land-use or climate data, primarily in disputed border regions with incomplete geospatial coverage (see dataset_summary.md).

4. **Single-year snapshot data.** Training features reflect current/recent averaged conditions (e.g., annual climatology), not multi-year historical trends — relevant context for the upcoming Investment Analysis module, which may require longer time horizons.

## Relevance to Investment Analysis (Next Module)

The dominant-driver behavior of these models means investment risk assessment should weight resource variability (solar/wind resource stability over time) more heavily than site-specific secondary factors when estimating revenue confidence — a consideration for the forecasting/investment module design.