from sqlalchemy import *

from app.core.database import Base


class CareerRole(Base):

    __tablename__ = "career_roles"

    id = Column(
        BigInteger,
        primary_key=True
    )

    title = Column(
        String(255),
        unique=True
    )

    category = Column(
        String(100)
    )

    description = Column(Text)

    education_level = Column(
        String(100)
    )

    average_salary_min = Column(
        DECIMAL(12,2)
    )

    average_salary_max = Column(
        DECIMAL(12,2)
    )

    demand_score = Column(
        DECIMAL(5,2)
    )

    growth_rate = Column(
        DECIMAL(5,2)
    )

    future_scope_score = Column(
        DECIMAL(5,2)
    )


class CareerRoleSkill(Base):

    __tablename__ = "career_role_skills"

    id = Column(
        BigInteger,
        primary_key=True
    )

    career_role_id = Column(
        BigInteger,
        ForeignKey("career_roles.id")
    )

    skill_id = Column(
        BigInteger,
        ForeignKey("skills.id")
    )

    importance_score = Column(
        DECIMAL(5,2)
    )

    is_mandatory = Column(
        Boolean,
        default=False
    )