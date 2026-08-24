class HardConstraints:
    def validate(self,feature):
        reasons = []
        if feature["slope"] > 30:
            reasons.append("Slope is too steep")
        if feature["solar"] < 3:
            reasons.append("Low solar irradiance")
        if feature["wind"] < 4:
            reasons.append("Low wind speed")
        if feature.get("restricted_land",False):
            reasons.append("Restricted land")
        feasible = len(reasons) == 0
        return feasible,reasons