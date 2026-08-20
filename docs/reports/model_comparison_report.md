# Model Comparison & Evaluation Report

In this phase, we trained two competing baseline algorithms to predict the `overall_score` (Site Suitability): **Decision Tree** vs **Random Forest**.

The synthetic dataset of 2,000 samples was split into three distinct subsets to ensure rigorous and unbiased evaluation:
- **Train (70%)**: Used by the algorithms to learn the patterns.
- **Validation (15%)**: Used to compare the models and check for overfitting.
- **Test (15%)**: Kept entirely unseen until the final winner was chosen, ensuring an unbiased final metric.

## 1. Performance Comparison Table

| Model | Subset | MAE | RMSE | R² Score |
| :--- | :--- | :--- | :--- | :--- |
| **Decision Tree** | Train | 0.00 | 0.00 | 100% |
| **Decision Tree** | Validation | 4.01 | 5.01 | 80.2% |
| **Random Forest** | Train | 1.18 | 1.46 | 98.2% |
| **Random Forest** | Validation | 3.05 | 3.76 | 88.8% |

## 2. Model Behavior Analysis (Overfitting vs Generalization)

### Decision Tree Analysis
- **Diagnosis: Severe Overfitting.**
- **Reasoning:** The Decision Tree achieved a perfect 0.0 MAE and 100% R² on the Training set. It memorized the training data perfectly. However, when presented with the Validation set (data it had never seen), its performance plummeted to 80.2% R², and errors spiked. This massive gap between Train and Validation performance is the textbook definition of overfitting.

### Random Forest Analysis
- **Diagnosis: Generalizing Well.**
- **Reasoning:** The Random Forest also learned the training data excellently (98.2% R²), but more importantly, it maintained a strong 88.8% R² on the Validation set. Because the gap between Train and Validation performance is much smaller, and the Validation metrics are significantly better than the Decision Tree's, we can conclude that the Random Forest generalized the underlying rules effectively instead of just memorizing noise.

## 3. Final Conclusion & Deployment
Because the **Random Forest** demonstrated superior generalization and significantly lower error on unseen data, it was automatically selected as the winning model by our training pipeline.

The winning model was then evaluated on the final 15% **Test Set** (which it had never seen during training or comparison).
**Final Test Metrics:**
- **MAE:** 2.80
- **RMSE:** 3.44
- **R² Score:** 90.7%

The model proved it is highly capable and stable. It has been serialized and persisted to `backend/models/best_baseline_model.joblib` for deployment into the FastAPI backend!
