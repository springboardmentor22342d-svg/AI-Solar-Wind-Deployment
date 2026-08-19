from app.services.energy_calculator import EnergyCalculator

calculator = EnergyCalculator()

solar_energy = calculator.calculate_solar_energy(
    installed_capacity=100,
    capacity_factor=0.25,
)

wind_energy = calculator.calculate_wind_energy(
    installed_capacity=100,
    capacity_factor=0.35,
)

print("Annual Solar Energy :", solar_energy, "kWh")

print("Annual Wind Energy :", wind_energy, "kWh")