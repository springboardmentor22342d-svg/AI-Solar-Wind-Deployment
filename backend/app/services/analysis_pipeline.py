from app.services.solar_services import SolarFeatureService
from app.services.wind_assessment import (
    calculate_capacity_factor,
    calculate_wind_class,
    classify_wind_site,
)
from app.evaluation.evaluator import Evaluator
from forecasting.forecasting_pipeline import ForecastingPipeline
from app.feasibility.feasibility_engine import FeasibilityEngine
from app.services.energy_yield_service import EnergyYieldService
from app.optimization.optimizer import OptimizationEngine 

class AnalysisPipeline:

    def __init__(self):
        self.solar_service = SolarFeatureService()
        self.evaluator = Evaluator()
        self.forecasting = ForecastingPipeline()
        self.feasibility = FeasibilityEngine()
        self.energy_service = EnergyYieldService()
        self.optimizer = OptimizationEngine()

    def analyze(
        self,
        latitude: float,
        longitude: float,
        date: str = "2025-01-06"
    ):

        # =====================================================
        # 1. GET SOLAR / WEATHER FEATURES
        # =====================================================

        solar = self.solar_service.get_features(
            latitude,
            longitude
        )

        # =====================================================
        # 2. EXTRACT FEATURES
        # =====================================================

        solar_irradiance = solar.get(
            "solar_irradiance",
            0
        )

        wind_speed = solar.get(
            "wind_speed",
            0
        )

        temperature = solar.get(
            "temperature",
            0
        )

        humidity = solar.get(
            "relative_humidity",
            0
        )

        # =====================================================
        # 3. CONVERT DICTIONARY VALUES TO AVERAGES
        # =====================================================

        if isinstance(solar_irradiance, dict):

            if solar_irradiance:
                solar_irradiance = (
                    sum(solar_irradiance.values())
                    / len(solar_irradiance)
                )
            else:
                solar_irradiance = 0

        if isinstance(wind_speed, dict):

            if wind_speed:
                wind_speed = (
                    sum(wind_speed.values())
                    / len(wind_speed)
                )
            else:
                wind_speed = 0

        if isinstance(temperature, dict):

            if temperature:
                temperature = (
                    sum(temperature.values())
                    / len(temperature)
                )
            else:
                temperature = 0

        if isinstance(humidity, dict):

            if humidity:
                humidity = (
                    sum(humidity.values())
                    / len(humidity)
                )
            else:
                humidity = 0

        # =====================================================
        # 4. WIND ASSESSMENT
        # =====================================================

        wind_capacity = calculate_capacity_factor(
            wind_speed
        )

        wind_class = calculate_wind_class(
            wind_speed
        )

        wind_site = classify_wind_site(
            wind_speed
        )

        # =====================================================
        # 5. SOLAR ENERGY GENERATION
        # =====================================================

        solar_energy = self.energy_service.calculate_solar_yield(
            solar_irradiance=solar_irradiance,
            installed_capacity=100,
            efficiency=0.85
        )

        # =====================================================
        # 6. WIND ENERGY GENERATION
        # =====================================================

        wind_energy = self.energy_service.calculate_wind_yield(
            installed_capacity=100,
            capacity_factor=wind_capacity,
            efficiency=0.90
        )

        # =====================================================
        # 7. TOTAL HYBRID ENERGY
        # =====================================================

        total_energy = self.energy_service.calculate_hybrid_yield(
            solar_energy=solar_energy,
            wind_energy=wind_energy
        )

        # =====================================================
        # 8. FEATURE DICTIONARY
        # =====================================================

        feature = {

            "site_id": 1,

            "latitude": latitude,

            "longitude": longitude,

            "solar": solar_irradiance,

            "wind": wind_speed,

            "temperature": temperature,

            "humidity": humidity,

            "wind_capacity_factor": wind_capacity,

            "wind_class": wind_class,

            "wind_site": wind_site,

            # Temporary GIS values
            "slope": 10,
            "grid": 5,
            "road": 2,
            "land_area": 50,
        }

        site = {
            "solar_capacity_factor": min(feature["solar"] / 5.0, 1.0),
            "wind_capacity_factor": wind_capacity,
            "land_area": feature["land_area"],
        }

        optimization = self.optimizer.optimize(site)

        # =====================================================
        # 10. FORECASTING
        # =====================================================

        forecast = self.forecasting.prepare_data(
            "data/historical_data.csv"
        )

        # =====================================================
        # 11. SITE EVALUATION
        # =====================================================

        evaluation = self.evaluator.evaluate(
            feature
        )

        # =====================================================
        # 12. RETURN RESULT
        # =====================================================

        return {

            "location": {

                "latitude": latitude,

                "longitude": longitude
            },

            "date": date,

            "solar_features": {

                "solar_irradiance": solar_irradiance,

                "temperature": temperature,

                "relative_humidity": humidity
            },

            "wind_features": {

                "wind_speed": wind_speed,

                "capacity_factor": wind_capacity,

                "wind_class": wind_class,

                "site_classification": wind_site
            },

            "energy_prediction": {

                "solar_energy_kwh_per_year":
                    solar_energy,

                "wind_energy_kwh_per_year":
                    wind_energy,

                "total_hybrid_energy_kwh_per_year":
                    total_energy
            },

            "evaluation": evaluation,

            "forecasting": forecast,

            "optimization": optimization
        }