from app.forecasting.forecast_input_pipeline import ForecastInputPipeline
from app.services.feature_engineering.feature_builder import create_feature_builder
from app.forecasting.hybrid_forecast import HybridForecastModel

builder = create_feature_builder()
pipeline = ForecastInputPipeline(builder)
df = pipeline.prepare_forecast_input(23.2599, 77.4126, "20230101", "20231231")

model = HybridForecastModel()
model.fit(df)
print(model.predict(6))   
print(model.predict(12))  