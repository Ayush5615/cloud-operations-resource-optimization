def detect_cost_anomaly(cost_data, threshold=0.30):
    """
    Detect a cost anomaly by comparing the latest daily cost
    against the average cost of previous days.

    An anomaly is flagged when the latest cost is
    30% or more above the historical average.
    """

    if not cost_data or len(cost_data) < 2:
        return {
            "anomaly_detected": False,
            "reason": "Insufficient cost history."
        }

    historical_data = cost_data[:-1]
    latest_data = cost_data[-1]

    historical_average = sum(
        item["daily_cost"] for item in historical_data
    ) / len(historical_data)

    latest_cost = latest_data["daily_cost"]

    increase_ratio = (
        (latest_cost - historical_average)
        / historical_average
        if historical_average > 0
        else 0
    )

    anomaly_detected = increase_ratio >= threshold

    return {
        "instance_id": latest_data["instance_id"],
        "latest_date": latest_data["date"],
        "latest_cost": round(latest_cost, 2),
        "historical_average": round(historical_average, 2),
        "increase_percentage": round(increase_ratio * 100, 2),
        "anomaly_detected": anomaly_detected
    }