OPERATING_HOURS = 8760
def estimate_solar_energy(installed_capacity,capacity_factor):
    """
    Estimate annual solar energy generation.
    Returns annual energy in kWh.
    """
    annual_energy = (
        installed_capacity * capacity_factor * OPERATING_HOURS
    )
    return annual_energy