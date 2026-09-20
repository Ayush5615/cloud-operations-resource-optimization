from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime, Text

from database import Base


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    resource_id = Column(String, nullable=False)
    service = Column(String, nullable=False)
    anomaly_percentage = Column(Float, nullable=False)
    reason = Column(Text, nullable=False)
    recommendation = Column(Text, nullable=False)
    estimated_monthly_saving = Column(Float, default=0.0)
    risk = Column(String, nullable=False)
    status = Column(String, default="PENDING_APPROVAL")
    created_at = Column(DateTime, default=datetime.utcnow)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    action = Column(String, nullable=False)
    resource_id = Column(String, nullable=False)
    approved_by = Column(String, nullable=False)
    before_state = Column(Text)
    after_state = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)