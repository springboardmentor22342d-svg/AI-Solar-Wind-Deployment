import joblib
import os


class FeatureImportance:

    FEATURES = [
        "month",
        "day",
        "day_of_year",
        "week_of_year",
        "temperature",
        "humidity",
        "wind_speed"
    ]

    def __init__(self):

        model_path = os.path.join(
            "models",
            "solar_random_forest.joblib"
        )

        self.model = joblib.load(model_path)

    def get_feature_importance(self):

        importance = self.model.feature_importances_

        ranking = []

        for feature, score in zip(
            self.FEATURES,
            importance
        ):

            ranking.append({

                "feature": feature,

                "importance": round(
                    float(score),
                    4
                )

            })

        ranking = sorted(

            ranking,

            key=lambda x: x["importance"],

            reverse=True

        )

        return ranking