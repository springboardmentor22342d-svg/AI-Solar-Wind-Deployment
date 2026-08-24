class SoftConstraints:
    def score(self,feature):
        score = 100
        if feature["road"] > 10:
            score -= 20
        if feature["grid"] > 15:
            score -= 20
        if feature["wind_capacity_factor"] < 0.4:
            score -= 20
        if score < 0:
            score = 0
        return score