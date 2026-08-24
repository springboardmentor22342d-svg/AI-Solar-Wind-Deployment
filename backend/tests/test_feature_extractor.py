import pandas as pd

from backend.app.forecasting.feature_extractor import (
    TimeFeatureExtractor
)


def test_feature_extraction():

    df = pd.DataFrame({
        "date": [
            "2024-01-01",
            "2024-02-15",
            "2024-03-20"
        ]
    })

    extractor = TimeFeatureExtractor()

    result = extractor.transform(df)

    assert "year" in result.columns
    assert "month" in result.columns
    assert "day" in result.columns
    assert "day_of_year" in result.columns
    assert "week" in result.columns


def test_year_values():

    df = pd.DataFrame({
        "date": ["2025-07-10"]
    })

    extractor = TimeFeatureExtractor()

    result = extractor.transform(df)

    assert result.loc[0, "year"] == 2025


def test_month_values():

    df = pd.DataFrame({
        "date": ["2025-12-25"]
    })

    extractor = TimeFeatureExtractor()

    result = extractor.transform(df)

    assert result.loc[0, "month"] == 12 