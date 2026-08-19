from sklearn.tree import DecisionTreeRegressor


class DecisionTreeModel:

    def __init__(self):

        self.model = DecisionTreeRegressor(
            random_state=42
        )

    def train(self, split_data):

        X_train = split_data["X_train"]
        y_train = split_data["y_train"]

        X_validation = split_data["X_validation"]
        X_test = split_data["X_test"]

        self.model.fit(
            X_train,
            y_train
        )

        training_predictions = self.model.predict(
            X_train
        )

        validation_predictions = self.model.predict(
            X_validation
        )

        test_predictions = self.model.predict(
            X_test
        )

        return {
            "model": self.model,
            "training_predictions": training_predictions,
            "validation_predictions": validation_predictions,
            "test_predictions": test_predictions
        }