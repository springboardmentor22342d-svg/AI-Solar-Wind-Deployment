class ModelBehaviorAnalyzer:

    def analyze(self, train_metrics, validation_metrics):

        difference = validation_metrics["MAE"] - train_metrics["MAE"]

        if difference >= 0.50:
            return "Severe Overfitting"

        elif difference >= 0.20:
            return "Moderate Overfitting"

        elif difference >= 0.05:
            return "Slight Overfitting"

        else:
            return "Generalizes Well"