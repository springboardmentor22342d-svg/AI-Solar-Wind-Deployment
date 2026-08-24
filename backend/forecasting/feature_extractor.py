import pandas as pd
class TimeFeatureExtractor:
    def extract_feature(self,data):
        data = data.copy()
        data["date"] = pd.to_datetime(data["date"])
        data["year"] = data["date"].dt.year
        data["month"] = data["date"].dt.month
        data["day"] = data["date"].dt.day
        data["day_of_year"] = data["date"].dt.dayofyear
        data["week_number"] = data["date"].dt.isocalendar().week
        return data
