def generate_ai_explanation(anomaly, cpu_utilization=None):
    """
    Mock AI explanation layer.

    This deterministic version simulates the structure
    that will later be returned by Gemini.
    """

    increase = anomaly.get("increase_percentage", 0)
    latest_cost = anomaly.get("latest_cost", 0)
    historical_average = anomaly.get("historical_average", 0)

    if increase >= 50:
        reason = (
            f"Daily cost increased by {increase}% compared with the "
            f"historical average of ${historical_average:.2f}."
        )

        recommendation = (
            "Review recent workload changes, resource utilization, "
            "and instance sizing before taking optimization action."
        )

        estimated_monthly_saving = round(
            max(latest_cost - historical_average, 0) * 30,
            2
        )

        risk = "Low"

    elif increase >= 30:
        reason = (
            f"Daily cost increased by {increase}% compared with the "
            f"historical baseline."
        )

        recommendation = (
            "Review resource utilization and recent workload changes."
        )

        estimated_monthly_saving = round(
            max(latest_cost - historical_average, 0) * 30,
            2
        )

        risk = "Low"

    else:
        reason = "No significant cost anomaly was detected."

        recommendation = (
            "Continue monitoring the resource for future changes."
        )

        estimated_monthly_saving = 0.0

        risk = "Low"

    return {
        "reason": reason,
        "recommendation": recommendation,
        "estimated_monthly_saving": estimated_monthly_saving,
        "risk": risk
    }