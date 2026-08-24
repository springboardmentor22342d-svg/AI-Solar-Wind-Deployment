OPERATING_HOURS = 8760
def estimate_wind_energy(installed_capacity,capacity_factor):
    """
    Estimate annual wind energy generation.
    Return annual energy in kWh.
    """
    annual_energy = (
        installed_capacity * capacity_factor * OPERATING_HOURS
    )
    return annual_energy