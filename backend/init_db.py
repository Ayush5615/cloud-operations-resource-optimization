from database import Base, engine
from models import Recommendation, AuditLog


Base.metadata.create_all(bind=engine)

print("Database initialized successfully.")
print("Tables created:")
print("- recommendations")
print("- audit_logs")