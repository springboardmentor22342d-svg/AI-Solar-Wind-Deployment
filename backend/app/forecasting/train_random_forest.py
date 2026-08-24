# train_random_forest.py

import os
import joblib
from sklearn.ensemble import RandomForestRegressor

class RandomForestForecastModel:

    def __init__(self):
        self.model = RandomForestRegressor(
            n_estimators=100,
            random_state=42
        )

    def train(self, X_train, y_train):
        
        self.model.fit(X_train, y_train)

    def save(self, model_path):
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        joblib.dump(self.model, model_path)

    def load(self, model_path):
        self.model = joblib.load(model_path)

    def predict(self, X):
        return self.model.predict(X)