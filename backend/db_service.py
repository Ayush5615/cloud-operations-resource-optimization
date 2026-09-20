from database import SessionLocal
from models import Recommendation, AuditLog


# --------------------------------------------------
# SAVE RECOMMENDATION
# --------------------------------------------------

def save_recommendation(
    resource_id,
    service,
    anomaly_percentage,
    reason,
    recommendation,
    estimated_monthly_saving,
    risk
):
    db = SessionLocal()

    try:
        new_recommendation = Recommendation(
            resource_id=resource_id,
            service=service,
            anomaly_percentage=anomaly_percentage,
            reason=reason,
            recommendation=recommendation,
            estimated_monthly_saving=estimated_monthly_saving,
            risk=risk,
            status="PENDING_APPROVAL"
        )

        db.add(new_recommendation)
        db.commit()
        db.refresh(new_recommendation)

        return new_recommendation

    finally:
        db.close()


# --------------------------------------------------
# GET ALL RECOMMENDATIONS
# --------------------------------------------------

def get_recommendations():
    db = SessionLocal()

    try:
        return db.query(Recommendation).order_by(
            Recommendation.created_at.desc()
        ).all()

    finally:
        db.close()


# --------------------------------------------------
# GET SINGLE RECOMMENDATION
# --------------------------------------------------

def get_recommendation(recommendation_id):
    db = SessionLocal()

    try:
        return db.query(Recommendation).filter(
            Recommendation.id == recommendation_id
        ).first()

    finally:
        db.close()


# --------------------------------------------------
# GET ACTIVE RECOMMENDATION
# --------------------------------------------------

def get_active_recommendation(resource_id):
    db = SessionLocal()

    try:
        return db.query(Recommendation).filter(
            Recommendation.resource_id == resource_id,
            Recommendation.status.in_([
                "PENDING_APPROVAL",
                "APPROVED"
            ])
        ).first()

    finally:
        db.close()


# --------------------------------------------------
# UPDATE RECOMMENDATION STATUS
# --------------------------------------------------

def update_recommendation_status(
    recommendation_id,
    status
):
    db = SessionLocal()

    try:
        recommendation = db.query(
            Recommendation
        ).filter(
            Recommendation.id == recommendation_id
        ).first()

        if recommendation is None:
            return None

        recommendation.status = status

        db.commit()
        db.refresh(recommendation)

        return recommendation

    finally:
        db.close()


# --------------------------------------------------
# SAVE AUDIT LOG
# --------------------------------------------------

def save_audit_log(
    action,
    resource_id,
    approved_by,
    before_state,
    after_state
):
    db = SessionLocal()

    try:
        audit = AuditLog(
            action=action,
            resource_id=resource_id,
            approved_by=approved_by,
            before_state=before_state,
            after_state=after_state
        )

        db.add(audit)
        db.commit()
        db.refresh(audit)

        return audit

    finally:
        db.close()


# --------------------------------------------------
# GET AUDIT LOGS
# --------------------------------------------------

def get_audit_logs():
    db = SessionLocal()

    try:
        return db.query(AuditLog).order_by(
            AuditLog.timestamp.desc()
        ).all()

    finally:
        db.close()