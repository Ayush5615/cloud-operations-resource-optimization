import boto3


def stop_ec2_instance(instance_id, mock=True):
    """
    Stop an EC2 instance.

    mock=True:
        Does not call AWS. Used for local development/testing.

    mock=False:
        Calls AWS EC2 StopInstances API.
    """

    if mock:
        return {
            "success": True,
            "action": "STOP_INSTANCE",
            "instance_id": instance_id,
            "mode": "MOCK",
            "message": f"Mock action: EC2 instance {instance_id} would be stopped."
        }

    ec2 = boto3.client("ec2")

    response = ec2.stop_instances(
        InstanceIds=[instance_id]
    )

    return {
        "success": True,
        "action": "STOP_INSTANCE",
        "instance_id": instance_id,
        "mode": "AWS",
        "message": f"EC2 instance {instance_id} stop request submitted.",
        "aws_response": response
    }