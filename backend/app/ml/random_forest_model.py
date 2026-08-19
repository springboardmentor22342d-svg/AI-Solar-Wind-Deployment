from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split


class RandomForestModel:

    def __init__(self):
        # Tuned hyperparameters for superior accuracy and reduced overfitting
        self.model = RandomForestRegressor(
            n_estimators=300,
            max_depth=10,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )

    def train(self, X_or_dict, y=None):
        if isinstance(X_or_dict, dict):
            X_train = X_or_dict["X_train"]
            y_train = X_or_dict["y_train"]
            X_val = X_or_dict.get("X_validation", X_train)
            X_test = X_or_dict.get("X_test", X_train)
            y_test = X_or_dict.get("y_test", y_train)
        else:
            X_train, X_test, y_train, y_test = train_test_split(
                X_or_dict, y, test_size=0.2, random_state=42
            )
            X_val = X_test

        self.model.fit(X_train, y_train)

        training_predictions = self.model.predict(X_train)
        validation_predictions = self.model.predict(X_val)
        test_predictions = self.model.predict(X_test)

        return {
            "model": self.model,
            "X_train": X_train,
            "X_test": X_test,
            "y_test": y_test,
            "predictions": test_predictions,
            "training_predictions": training_predictions,
            "validation_predictions": validation_predictions,
            "test_predictions": test_predictions
        }