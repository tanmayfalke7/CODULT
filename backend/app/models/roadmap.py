from sqlalchemy import *

from app.core.database import Base


class CareerRoadmap(Base):

    __tablename__ = "career_roadmaps"

    id = Column(
        BigInteger,
        primary_key=True
    )

    session_id = Column(
        BigInteger,
        ForeignKey(
            "recommendation_sessions.id"
        )
    )

    career_recommendation_id = Column(
        BigInteger,
        ForeignKey(
            "career_recommendations.id"
        )
    )

    roadmap_title = Column(
        String(255)
    )

    roadmap_content = Column(Text)

    roadmap_json = Column(JSON)

    estimated_duration_months = Column(
        Integer
    )

    generated_by_model = Column(
        String(255)
    )


class RoadmapStep(Base):

    __tablename__ = "roadmap_steps"

    id = Column(
        BigInteger,
        primary_key=True
    )

    roadmap_id = Column(
        BigInteger,
        ForeignKey(
            "career_roadmaps.id"
        )
    )

    step_order = Column(Integer)

    title = Column(String(255))

    description = Column(Text)

    estimated_duration_days = Column(
        Integer
    )

    resource_links = Column(JSON)


class UserRoadmapProgress(Base):

    __tablename__ = "user_roadmap_progress"

    id = Column(
        BigInteger,
        primary_key=True
    )

    user_id = Column(
        BigInteger,
        ForeignKey("users.id")
    )

    roadmap_step_id = Column(
        BigInteger,
        ForeignKey("roadmap_steps.id")
    )

    status = Column(
        Enum(
            "not_started",
            "in_progress",
            "completed",
            name="progress_enum"
        ),
        default="not_started"
    )

    completion_percentage = Column(
        Integer,
        default=0
    )
