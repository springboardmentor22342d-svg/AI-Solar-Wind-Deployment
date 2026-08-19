# Random Forest Model Documentation

## Selected Model

Random Forest Regressor

The Random Forest model was selected after comparing its performance with a Decision Tree model.

---

## Evaluation Metrics

Training

- MAE : 0.1964
- RMSE : 0.2638
- R² : 0.9579
- MAPE : 4.87%

Validation

- MAE : 0.5395
- RMSE : 0.7200
- R² : 0.5728
- MAPE : 11.84%

---

## Most Influential Features

| Feature | Importance |
|---------|-----------:|
| Humidity | 0.5267 |
| Wind Speed | 0.1591 |
| Day of Year | 0.1153 |
| Temperature | 0.1074 |
| Day | 0.0416 |
| Week of Year | 0.0402 |
| Month | 0.0098 |

---

## Behaviour

The Random Forest model demonstrates moderate overfitting. Training performance is significantly better than validation performance, but it still generalizes much better than the Decision Tree model.

---

## Limitations

- Dataset contains approximately 1,096 historical observations.
- Only one geographical dataset has been used.
- No hyperparameter tuning has been performed.
- Forecasting currently relies on historical weather patterns only.
- Future improvements include cross-validation, XGBoost integration, larger datasets, and hyperparameter optimization.