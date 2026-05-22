import uuid

from sqlalchemy.orm import Session

from app.models.recommendation import (
    RecommendationSession,
    CareerRecommendation
)

from app.models.career import (
    CareerRole
)

from app.services.activity_service import (
    create_activity
)


def create_recommendation_session(
    db: Session,
    user_id: int,
    resume_id: int
):

    session = RecommendationSession(
        uuid=str(uuid.uuid4()),
        user_id=user_id,
        resume_id=resume_id,
        recommendation_model="LogisticRegression",
        embedding_model="SBERT all-MiniLM-L6-v2",
        llm_model="llama3-70b-8192"
    )

    db.add(session)

    db.commit()

    db.refresh(session)

    return session


def get_or_create_career_role(
    db: Session,
    career_title: str
):

    role = db.query(
        CareerRole
    ).filter(
        CareerRole.title == career_title
    ).first()

    if role:

        return role

    role = CareerRole(
        title=career_title,
        category="AI/ML"
    )

    db.add(role)

    db.commit()

    db.refresh(role)

    return role


def save_career_recommendations(
    db: Session,
    session_id: int,
    recommendations: list,
    user_id: int
):

    saved_recommendations = []

    for index, recommendation in enumerate(
        recommendations
    ):

        role = get_or_create_career_role(
            db,
            recommendation["career"]
        )

        recommendation_entry = (
            CareerRecommendation(
                session_id=session_id,
                career_role_id=role.id,
                recommendation_rank=index + 1,
                match_score=recommendation[
                    "similarity_score"
                ] * 100,
                recommendation_reason=f"""
                Strong match based on
                skills and interests
                """
            )
        )

        db.add(recommendation_entry)

        saved_recommendations.append(
            recommendation_entry
        )

    db.commit()

    create_activity(
        db=db,
        user_id=user_id,
        activity_type="career_recommendation",
        activity_description="""
        Generated AI career recommendations
        """
    )

    return saved_recommendations