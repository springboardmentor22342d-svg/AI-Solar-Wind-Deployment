class HybridYieldEstimator:

    def estimate(

        self,

        solar_energy,

        wind_energy

    ):

        hybrid_energy = (

            solar_energy +

            wind_energy

        )

        return round(

            hybrid_energy,

            2

        )