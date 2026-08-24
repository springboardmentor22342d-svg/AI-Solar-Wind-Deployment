def recommend_strategy(site):
    solar = site.get("solar_capacity_factor",0)
    wind = site.get("wind_capacity_factor",0)
    if solar >= 0.20 and wind >= 0.35:
        return "Hybrid"
    elif solar >= wind:
        return "Solar"
    else:
        return "Wind"