from datetime import date, timedelta


def get_mock_cost_data(instance_id):
    """
    Generate 14 days of simulated daily cost data for an EC2 instance.

    The first 13 days represent normal/stable usage.
    The latest day contains a deliberate cost spike
    so that our anomaly detection logic can be tested.
    """

    today = date.today()
    cost_data = []

    # 13 days of stable cost
    for days_ago in range(13, 0, -1):
        current_date = today - timedelta(days=days_ago)

        cost_data.append({
            "instance_id": instance_id,
            "date": current_date.isoformat(),
            "daily_cost": 0.80
        })

    # Latest day with deliberate spike
    cost_data.append({
        "instance_id": instance_id,
        "date": today.isoformat(),
        "daily_cost": 1.20
    })

    return cost_data