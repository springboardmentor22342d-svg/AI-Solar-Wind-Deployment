class DeploymentOptimizer:

    def determine_strategy(self, site):
        solar = site.get("solar_score", 0)
        wind = site.get("wind_score", 0)
        overall = site.get("overall_score", 0)

        if solar >= 75 and wind >= 75:
            deployment = "Hybrid"
            confidence = min(overall + 5, 100)
            reason = "Both solar and wind resources are suitable for hybrid deployment."

        elif solar >= 75 and wind < 70:
            deployment = "Solar"
            confidence = solar
            reason = "High solar resource makes solar deployment the best option."

        elif wind >= 75 and solar < 70:
            deployment = "Wind"
            confidence = wind
            reason = "Strong wind resource makes wind deployment the best option."

        elif solar >= wind:
            deployment = "Solar"
            confidence = solar
            reason = "Solar resource performs better than wind."

        else:
            deployment = "Wind"
            confidence = wind
            reason = "Wind resource performs better than solar."

        return {
            "deployment": deployment,
            "confidence": confidence,
            "reason": reason,
        }