from sqlalchemy import *

from app.core.database import Base


class DashboardAnalytics(Base):

    __tablename__ = "dashboard_analytics"

    id = Column(
        BigInteger,
        primary_key=True
    )

    user_id = Column(
        BigInteger,
        ForeignKey("users.id")
    )

    total_resumes_uploaded = Column(
        Integer,
        default=0
    )

    total_recommendations_generated = Column(
        Integer,
        default=0
    )

    completed_roadmap_steps = Column(
        Integer,
        default=0
    )

    active_roadmaps = Column(
        Integer,
        default=0
    )

    top_career_domain = Column(
        String(255)
    )