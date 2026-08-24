OPERATING_HOURS_PER_YEAR = 8760


def estimate_annual_solar_energy(
    installed_capacity: float,
    capacity_factor: float
) -> float:
    """
    Estimate annual solar energy generation.

    Args:
        installed_capacity: Solar plant capacity in MW.
        capacity_factor: Capacity factor as a decimal (0 to 1).

    Returns:
        Estimated annual energy generation in MWh.
    """

    if installed_capacity < 0:
        raise ValueError("Installed capacity cannot be negative.")

    if not 0 <= capacity_factor <= 1:
        raise ValueError(
            "Capacity factor must be between 0 and 1."
        )

    annual_energy = (
        installed_capacity
        * capacity_factor
        * OPERATING_HOURS_PER_YEAR
    )

    return annual_energy