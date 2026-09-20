def analyze_ec2_resources(instances, cpu_data):
    recommendations = []

    for instance in instances:
        instance_id = instance["instance_id"]
        cpu = cpu_data.get(instance_id)

        if instance["state"] == "running":
            if cpu is not None and cpu < 10:
                recommendations.append({
                    "instance_id": instance_id,
                    "cpu_utilization": cpu,
                    "recommendation": "Consider downsizing or stopping the instance after validating workload requirements.",
                    "reason": f"Average CPU utilization is only {cpu}%, indicating potential underutilization.",
                    "priority": "High"
                })

            elif cpu is not None and cpu < 30:
                recommendations.append({
                    "instance_id": instance_id,
                    "cpu_utilization": cpu,
                    "recommendation": "Review instance sizing and workload utilization.",
                    "reason": f"Average CPU utilization is {cpu}%, which may indicate underutilization.",
                    "priority": "Medium"
                })

            else:
                recommendations.append({
                    "instance_id": instance_id,
                    "cpu_utilization": cpu,
                    "recommendation": "Continue monitoring resource utilization.",
                    "reason": f"Average CPU utilization is {cpu}%.",
                    "priority": "Low"
                })

    return recommendations