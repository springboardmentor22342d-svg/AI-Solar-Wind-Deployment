# Model Behaviour Documentation

## Selected Model
Random Forest Regressor

## Evaluation Metrics

| Metric | Value |
|--------|-------|
| MAE | 0.14 |
| RMSE | 0.14 |
| R² Score | 0.79 |

*(Replace these values with the ones from your own training output if they are different.)*

---

## Most Important Features

1. Wind Speed
2. Temperature
3. Humidity
4. Month
5. Day
6. Year
7. Day of Year

---

## Model Explanation

The prediction engine uses a trained Random Forest Regression model.

For every prediction, the API returns:

- Predicted Solar Irradiance
- Most important features
- Explanation of which features influenced the prediction

This makes the prediction easier to understand instead of returning only a number.

---

## Limitations

- Model trained on a small dataset.
- Accuracy will improve with more historical data.
- Feature importance represents overall model behaviour, not individual predictions.
- Weather conditions may vary in real-world scenarios.