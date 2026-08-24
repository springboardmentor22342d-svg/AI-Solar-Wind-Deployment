import pytest

from backend.app.energy.wind_estimation import (
    estimate_annual_wind_energy
)


def test_annual_wind_energy_calculation():

    result = estimate_annual_wind_energy(
        installed_capacity=100,
        capacity_factor=0.35
    )

    assert result == 306600


def test_zero_capacity():

    result = estimate_annual_wind_energy(
        installed_capacity=0,
        capacity_factor=0.35
    )

    assert result == 0


def test_invalid_capacity_factor():

    with pytest.raises(ValueError):

        estimate_annual_wind_energy(
            installed_capacity=100,
            capacity_factor=1.5
        )


def test_negative_capacity():

    with pytest.raises(ValueError):

        estimate_annual_wind_energy(
            installed_capacity=-100,
            capacity_factor=0.35
        )