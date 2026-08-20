from datetime import datetime
from typing import Dict, Any, List

class TemporalFeatureExtractor:
    """
    Derives useful temporal attributes from date columns for forecasting models.
    """

    @staticmethod
    def extract_features(date_str: str) -> Dict[str, int]:
        """
        Parses a 'YYYYMMDD' string and extracts temporal features.
        """
        try:
            dt = datetime.strptime(date_str, "%Y%m%d")
            return {
                "year": dt.year,
                "month": dt.month,
                "day": dt.day,
                "day_of_year": dt.timetuple().tm_yday,
                "week_number": dt.isocalendar()[1]
            }
        except ValueError:
            return {
                "year": 0, "month": 0, "day": 0, "day_of_year": 0, "week_number": 0
            }

    @staticmethod
    def transform_series(time_series: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Takes a time series (list of dicts) containing a 'date' key,
        and returns a new list with temporal features appended to each record.
        """
        transformed = []
        for record in time_series:
            new_record = record.copy()
            if "date" in new_record:
                temporal_features = TemporalFeatureExtractor.extract_features(new_record["date"])
                new_record.update(temporal_features)
            transformed.append(new_record)
        return transformed
