from sqlalchemy import *

from app.core.database import Base


class Skill(Base):

    __tablename__ = "skills"

    id = Column(
        BigInteger,
        primary_key=True
    )

    name = Column(
        String(255),
        unique=True
    )

    category = Column(
        String(100)
    )

    demand_score = Column(
        DECIMAL(5,2)
    )

    trend_direction = Column(
        Enum(
            "rising",
            "stable",
            "declining",
            name="trend_enum"
        )
    )


class UserSkill(Base):

    __tablename__ = "user_skills"

    id = Column(
        BigInteger,
        primary_key=True
    )

    user_id = Column(
        BigInteger,
        ForeignKey("users.id")
    )

    resume_id = Column(
        BigInteger,
        ForeignKey("resumes.id")
    )

    skill_id = Column(
        BigInteger,
        ForeignKey("skills.id")
    )

    proficiency_level = Column(
        Enum(
            "beginner",
            "intermediate",
            "advanced",
            "expert",
            name="proficiency_enum"
        )
    )

    extraction_confidence = Column(
        DECIMAL(5,2)
    )