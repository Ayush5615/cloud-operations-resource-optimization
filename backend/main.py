from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from aws_service import get_ec2_instances, get_cpu_utilization
from optimizer import analyze_ec2_resources
from cost_service import get_mock_cost_data
from anomaly_detector import detect_cost_anomaly
from ai_service import generate_ai_explanation

from remediation_service import stop_ec2_instance

from db_service import (
    save_recommendation,
    get_recommendations,
    get_recommendation,
    get_active_recommendation,
    update_recommendation_status,
    save_audit_log,
    get_audit_logs
)


# --------------------------------------------------
# APPLICATION
# --------------------------------------------------

app = FastAPI(
    title="Cloud Operations & Resource Optimization Platform",
    version="1.4.0"
)


# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# --------------------------------------------------
# ROOT
# --------------------------------------------------

@app.get("/")
def root():

    return {
        "message": "Cloud Operations Platform API is running",
        "version": "1.4.0"
    }


# --------------------------------------------------
# EC2 RESOURCES
# --------------------------------------------------

@app.get("/api/resources/ec2")
def get_ec2_resources():

    instances = get_ec2_instances()

    resources = []

    for instance in instances:

        instance_id = instance["instance_id"]

        cpu = get_cpu_utilization(
            instance_id
        )

        resources.append({

            "instance_id": (
                instance.get("instance_id")
            ),

            "instance_type": (
                instance.get("instance_type")
            ),

            "state": (
                instance.get("state")
            ),

            "availability_zone": (
                instance.get("availability_zone")
            ),

            "region": (
                instance.get("region")
            ),

            "cpu_utilization": cpu
        })

    return {
        "resource_type": "EC2",
        "resources": resources
    }


# --------------------------------------------------
# EC2 OPTIMIZATION
# --------------------------------------------------

@app.get("/api/optimization/ec2")
def get_ec2_optimization():

    instances = get_ec2_instances()

    cpu_data = {}

    for instance in instances:

        instance_id = instance["instance_id"]

        cpu_data[instance_id] = get_cpu_utilization(
            instance_id
        )

    recommendations = analyze_ec2_resources(
        instances,
        cpu_data
    )

    enriched_recommendations = []

    for item in recommendations:

        instance_id = (
            item.get("instance_id")
            or item.get("resource_id")
        )

        cost_data = get_mock_cost_data(
            instance_id
        )

        anomaly = detect_cost_anomaly(
            cost_data
        )

        enriched_recommendations.append({

            "instance_id": instance_id,

            "resource_id": instance_id,

            "cpu_utilization": (
                item.get("cpu_utilization")
            ),

            "anomaly_percentage": (
                anomaly.get(
                    "increase_percentage",
                    0
                )
            ),

            "recommendation": (
                item.get(
                    "recommendation",
                    "Review resource utilization."
                )
            ),

            "reason": (
                item.get(
                    "reason",
                    "Resource utilization should be reviewed."
                )
            ),

            "priority": (
                item.get(
                    "priority",
                    "Medium"
                )
            )
        })

    return {

        "resource_type": "EC2",

        "recommendations": (
            enriched_recommendations
        )
    }


# --------------------------------------------------
# EC2 ANOMALIES
# --------------------------------------------------

@app.get("/api/anomalies/ec2")
def get_ec2_anomalies():

    instances = get_ec2_instances()

    anomalies = []

    for instance in instances:

        instance_id = instance["instance_id"]

        cost_data = get_mock_cost_data(
            instance_id
        )

        anomaly = detect_cost_anomaly(
            cost_data
        )

        if anomaly.get("anomaly_detected"):

            cpu = get_cpu_utilization(
                instance_id
            )

            ai_explanation = generate_ai_explanation(
                anomaly,
                cpu
            )

            anomaly["cpu_utilization"] = cpu

            anomaly["ai_explanation"] = (
                ai_explanation
            )

        anomalies.append(anomaly)

    return {
        "resource_type": "EC2",
        "anomalies": anomalies
    }


# --------------------------------------------------
# CLOUD RESOURCE SCAN
# --------------------------------------------------

@app.post("/api/scan")
def run_scan():

    instances = get_ec2_instances()

    saved_recommendations = []

    for instance in instances:

        instance_id = instance["instance_id"]

        # Check whether an active recommendation
        # already exists for this resource.
        existing = get_active_recommendation(
            instance_id
        )

        if existing is not None:
            continue

        cost_data = get_mock_cost_data(
            instance_id
        )

        anomaly = detect_cost_anomaly(
            cost_data
        )

        if not anomaly.get("anomaly_detected"):
            continue

        cpu = get_cpu_utilization(
            instance_id
        )

        ai_explanation = generate_ai_explanation(
            anomaly,
            cpu
        )

        saved = save_recommendation(

            resource_id=instance_id,

            service="EC2",

            anomaly_percentage=(
                anomaly["increase_percentage"]
            ),

            reason=(
                ai_explanation["reason"]
            ),

            recommendation=(
                ai_explanation["recommendation"]
            ),

            estimated_monthly_saving=(
                ai_explanation[
                    "estimated_monthly_saving"
                ]
            ),

            risk=(
                ai_explanation["risk"]
            )
        )

        saved_recommendations.append({

            "id": saved.id,

            "resource_id": (
                saved.resource_id
            ),

            "service": saved.service,

            "status": saved.status
        })

    return {

        "message": (
            "Cloud resource scan completed"
        ),

        "recommendations_created": (
            len(saved_recommendations)
        ),

        "recommendations": (
            saved_recommendations
        )
    }


# --------------------------------------------------
# LIST RECOMMENDATIONS
# --------------------------------------------------

@app.get("/api/recommendations")
def list_recommendations():

    recommendations = get_recommendations()

    return {

        "count": len(recommendations),

        "recommendations": [

            {

                "id": item.id,

                "resource_id": (
                    item.resource_id
                ),

                "service": item.service,

                "anomaly_percentage": (
                    item.anomaly_percentage
                ),

                "reason": item.reason,

                "recommendation": (
                    item.recommendation
                ),

                "estimated_monthly_saving": (
                    item.estimated_monthly_saving
                ),

                "risk": item.risk,

                "status": item.status,

                "created_at": item.created_at
            }

            for item in recommendations
        ]
    }


# --------------------------------------------------
# GET SINGLE RECOMMENDATION
# --------------------------------------------------

@app.get(
    "/api/recommendations/{recommendation_id}"
)
def get_single_recommendation(
    recommendation_id: int
):

    recommendation = get_recommendation(
        recommendation_id
    )

    if recommendation is None:

        raise HTTPException(
            status_code=404,
            detail="Recommendation not found"
        )

    return {

        "id": recommendation.id,

        "resource_id": (
            recommendation.resource_id
        ),

        "service": recommendation.service,

        "anomaly_percentage": (
            recommendation.anomaly_percentage
        ),

        "reason": recommendation.reason,

        "recommendation": (
            recommendation.recommendation
        ),

        "estimated_monthly_saving": (
            recommendation.estimated_monthly_saving
        ),

        "risk": recommendation.risk,

        "status": recommendation.status,

        "created_at": recommendation.created_at
    }


# --------------------------------------------------
# APPROVE + REMEDIATE
# --------------------------------------------------

@app.post(
    "/api/recommendations/{recommendation_id}/approve"
)
def approve_recommendation(
    recommendation_id: int
):

    recommendation = get_recommendation(
        recommendation_id
    )

    if recommendation is None:

        raise HTTPException(
            status_code=404,
            detail="Recommendation not found"
        )

    if recommendation.status != "PENDING_APPROVAL":

        raise HTTPException(
            status_code=400,
            detail=(
                "Recommendation cannot be approved "
                f"from status {recommendation.status}"
            )
        )

    # Save state before remediation
    before_state = recommendation.status

    # Perform remediation
    remediation_result = stop_ec2_instance(
    recommendation.resource_id,
    mock=False
    )

    # Update recommendation status
    updated = update_recommendation_status(
        recommendation_id,
        "APPROVED"
    )

    # Save audit log
    audit = save_audit_log(
        action="STOP_INSTANCE",
        resource_id=recommendation.resource_id,
        approved_by="admin",
        before_state=before_state,
        after_state="APPROVED"
    )

    return {

        "message": (
            "Recommendation approved successfully"
        ),

        "id": updated.id,

        "status": updated.status,

        "remediation": remediation_result,

        "audit_logged": True,

        "audit_log_id": audit.id
    }


# --------------------------------------------------
# REJECT RECOMMENDATION
# --------------------------------------------------

@app.post(
    "/api/recommendations/{recommendation_id}/reject"
)
def reject_recommendation(
    recommendation_id: int
):

    recommendation = update_recommendation_status(
        recommendation_id,
        "REJECTED"
    )

    if recommendation is None:

        raise HTTPException(
            status_code=404,
            detail="Recommendation not found"
        )

    return {

        "message": (
            "Recommendation rejected"
        ),

        "id": recommendation.id,

        "status": recommendation.status
    }


# --------------------------------------------------
# AUDIT LOG
# --------------------------------------------------

@app.get("/api/audit-log")
def list_audit_logs():

    logs = get_audit_logs()

    return {

        "count": len(logs),

        "audit_logs": [

            {

                "id": log.id,

                "action": log.action,

                "resource_id": (
                    log.resource_id
                ),

                "approved_by": (
                    log.approved_by
                ),

                "before_state": (
                    log.before_state
                ),

                "after_state": (
                    log.after_state
                ),

                "timestamp": log.timestamp
            }

            for log in logs
        ]
    }