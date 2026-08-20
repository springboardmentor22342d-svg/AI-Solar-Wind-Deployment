import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class WindForecaster:
    """
    Predicts future wind speeds based on historical data.
    """
    def forecast(self, historical_data: List[Dict[str, Any]], days_ahead: int = 30) -> List[Dict[str, Any]]:
        """
        Uses a lightweight heuristic (historical average matching the day of year)
        to project future wind potential.
        """
        if not historical_data:
            return []

        day_of_year_averages = {}
        day_counts = {}

        for record in historical_data:
            doy = record.get("day_of_year")
            val = record.get("wind_speed")
            if doy is not None and val is not None:
                day_of_year_averages[doy] = day_of_year_averages.get(doy, 0) + val
                day_counts[doy] = day_counts.get(doy, 0) + 1

        for doy in day_of_year_averages:
            day_of_year_averages[doy] /= day_counts[doy]

        try:
            from datetime import datetime, timedelta
            last_date_str = historical_data[-1].get("date")
            last_date = datetime.strptime(last_date_str, "%Y%m%d")
        except Exception:
            last_date = datetime.utcnow()

        predictions = []
        global_avg = sum(day_of_year_averages.values()) / max(1, len(day_of_year_averages))

        for i in range(1, days_ahead + 1):
            target_date = last_date + timedelta(days=i)
            target_doy = target_date.timetuple().tm_yday
            
            predicted_wind = day_of_year_averages.get(target_doy, global_avg)

            predictions.append({
                "date": target_date.strftime("%Y%m%d"),
                "predicted_wind_speed": round(predicted_wind, 2)
            })

        return predictions
