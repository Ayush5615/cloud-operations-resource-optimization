import boto3
from datetime import datetime, timedelta, timezone


# --------------------------------------------------
# GET AWS EC2 INSTANCES
# --------------------------------------------------

def get_ec2_instances():

    ec2 = boto3.client("ec2")

    response = ec2.describe_instances()

    instances = []

    for reservation in response.get("Reservations", []):

        for instance in reservation.get("Instances", []):

            availability_zone = (
                instance.get("Placement", {})
                .get("AvailabilityZone")
            )

            # Example:
            # ap-south-1b -> ap-south-1
            # us-east-1a  -> us-east-1
            region = None

            if availability_zone:
                region = availability_zone[:-1]

            instances.append({

                "instance_id": (
                    instance.get("InstanceId")
                ),

                "instance_type": (
                    instance.get("InstanceType")
                ),

                "state": (
                    instance.get("State", {})
                    .get("Name")
                ),

                "availability_zone": (
                    availability_zone
                ),

                "region": region
            })

    return instances


# --------------------------------------------------
# GET EC2 CPU UTILIZATION
# --------------------------------------------------

def get_cpu_utilization(instance_id):

    cloudwatch = boto3.client("cloudwatch")

    end_time = datetime.now(timezone.utc)

    start_time = (
        end_time - timedelta(hours=24)
    )

    response = cloudwatch.get_metric_statistics(

        Namespace="AWS/EC2",

        MetricName="CPUUtilization",

        Dimensions=[
            {
                "Name": "InstanceId",
                "Value": instance_id
            }
        ],

        StartTime=start_time,

        EndTime=end_time,

        Period=3600,

        Statistics=[
            "Average"
        ]
    )

    datapoints = response.get(
        "Datapoints",
        []
    )

    # CloudWatch may temporarily have
    # no datapoints available.
    if not datapoints:
        return None

    cpu_values = []

    for point in datapoints:

        average = point.get(
            "Average"
        )

        if average is not None:
            cpu_values.append(
                float(average)
            )

    if not cpu_values:
        return None

    average_cpu = (
        sum(cpu_values)
        / len(cpu_values)
    )

    return round(
        average_cpu,
        2
    )