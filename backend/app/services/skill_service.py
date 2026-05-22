from sqlalchemy.orm import Session

from app.models.skill import (
    Skill,
    UserSkill
)


def get_or_create_skill(
    db: Session,
    skill_name: str
):

    existing_skill = db.query(
        Skill
    ).filter(
        Skill.name == skill_name
    ).first()

    if existing_skill:

        return existing_skill

    new_skill = Skill(
        name=skill_name
    )

    db.add(new_skill)

    db.commit()

    db.refresh(new_skill)

    return new_skill


def save_user_skills(
    db: Session,
    user_id: int,
    resume_id: int,
    skills: list
):

    saved_skills = []

    for skill_name in skills:

        skill = get_or_create_skill(
            db,
            skill_name.strip()
        )

        user_skill = UserSkill(
            user_id=user_id,
            resume_id=resume_id,
            skill_id=skill.id,
            proficiency_level="intermediate",
            extraction_confidence=0.90
        )

        db.add(user_skill)

        saved_skills.append(skill.name)

    db.commit()

    return saved_skills