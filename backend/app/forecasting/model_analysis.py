class ModelAnalysis:

    def analyze(
        self,
        train_r2,
        validation_r2
    ):
        """
        Analyze model behavior using training and validation R² scores.
        """

        gap = train_r2 - validation_r2

        if train_r2 < 0.70 and validation_r2 < 0.70:
            return "Underfitting"

        elif gap > 0.15:
            return "Overfitting"

        else:
            return "Generalizing Well"