from decimal import Decimal

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.skill import Skill, UserSkill
from app.models.user import User

router = APIRouter(
    prefix="/skills",
    tags=["Skills"]
)


def _decimal(value) -> float | None:

    if isinstance(value, Decimal):

        return float(value)

    return value


def serialize_skill(skill: Skill) -> dict:

    return {
        "id": skill.id,
        "name": skill.name,
        "category": skill.category,
        "demand_score": _decimal(skill.demand_score),
        "trend_direction": skill.trend_direction
    }


@router.get("")
def list_skills(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    skills = db.query(Skill).order_by(
        Skill.name
    ).all()

    return [
        serialize_skill(skill)
        for skill in skills
    ]


@router.get("/trending")
def trending_skills(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    rows = db.query(
        Skill,
        func.count(UserSkill.id).label("usage_count")
    ).outerjoin(
        UserSkill,
        UserSkill.skill_id == Skill.id
    ).group_by(
        Skill.id
    ).order_by(
        Skill.demand_score.desc(),
        func.count(UserSkill.id).desc()
    ).limit(20).all()

    return [
        {
            **serialize_skill(skill),
            "usage_count": usage_count
        }
        for skill, usage_count in rows
    ]


@router.get("/user")
def user_skills(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    rows = db.query(
        UserSkill,
        Skill
    ).join(
        Skill,
        Skill.id == UserSkill.skill_id
    ).filter(
        UserSkill.user_id == current_user.id
    ).all()

    return [
        {
            "id": user_skill.id,
            "resume_id": user_skill.resume_id,
            "proficiency_level": user_skill.proficiency_level,
            "extraction_confidence": _decimal(
                user_skill.extraction_confidence
            ),
            "skill": serialize_skill(skill)
        }
        for user_skill, skill in rows
    ]
