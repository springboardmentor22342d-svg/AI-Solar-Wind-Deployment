from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor


class BaselineModels:

    def train_decision_tree(
        self,
        X_train,
        y_train
    ):

        model = DecisionTreeRegressor(
            random_state=42
        )

        model.fit(
            X_train,
            y_train
        )

        return model

    def train_random_forest(
        self,
        X_train,
        y_train
    ):

        model = RandomForestRegressor(
            n_estimators=100,
            random_state=42
        )

        model.fit(
            X_train,
            y_train
        )

        return model