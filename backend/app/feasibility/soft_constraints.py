class SoftConstraintScorer:

    def score(self, site):

        score = 0

        remarks = []

        # Distance to Grid (30 Marks)
        if site["distance_to_grid"] <= 2:
            score += 30
            remarks.append("Excellent grid connectivity.")

        elif site["distance_to_grid"] <= 5:
            score += 20
            remarks.append("Moderate grid connectivity.")

        else:
            score += 10
            remarks.append("Poor grid connectivity.")

        # Distance to Road (20 Marks)
        if site["distance_to_road"] <= 1:
            score += 20
            remarks.append("Excellent road access.")

        elif site["distance_to_road"] <= 3:
            score += 15
            remarks.append("Moderate road access.")

        else:
            score += 5
            remarks.append("Poor road accessibility.")

        # Economic Rating (25 Marks)
        economic = site["economic_rating"] * 25 / 100
        score += economic

        # Environmental Rating (25 Marks)
        environmental = site["environmental_rating"] * 25 / 100
        score += environmental

        return {

            "score": round(score, 2),

            "remarks": remarks

        }