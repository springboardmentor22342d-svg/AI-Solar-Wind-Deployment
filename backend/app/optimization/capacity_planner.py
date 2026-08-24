
class CapacityPlanner:

    def estimate_capacity(self, site):
        land_area = site.get("land_area", 0)
        deployment = site.get("deployment", "Solar")

        if land_area < 20:
            capacity = 5

        elif land_area < 50:
            capacity = 10

        elif land_area < 100:
            capacity = 25

        elif land_area < 200:
            capacity = 50

        else:
            capacity = 100

        return {
            "deployment": deployment,
            "recommended_capacity": capacity,
            "unit": "MW"
        }

