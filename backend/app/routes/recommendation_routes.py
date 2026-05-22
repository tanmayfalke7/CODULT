from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.career import CareerRole
from app.models.recommendation import (
    CareerRecommendation,
    RecommendationSession
)
from app.models.user import User

router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"]
)


def _score(value) -> float:

    if isinstance(value, Decimal):

        return float(value)

    return value or 0


def serialize_recommendation(
    recommendation: CareerRecommendation,
    role: CareerRole | None = None
) -> dict:

    return {
        "id": recommendation.id,
        "session_id": recommendation.session_id,
        "career_role_id": recommendation.career_role_id,
        "career_title": role.title if role else None,
        "rank": recommendation.recommendation_rank,
        "match_score": _score(
            recommendation.match_score
        ),
        "reason": recommendation.recommendation_reason
    }


@router.get("")
def latest_recommendations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    session = db.query(RecommendationSession).filter(
        RecommendationSession.user_id == current_user.id
    ).order_by(
        RecommendationSession.id.desc()
    ).first()

    if not session:

        return []

    rows = db.query(
        CareerRecommendation,
        CareerRole
    ).join(
        CareerRole,
        CareerRole.id == CareerRecommendation.career_role_id
    ).filter(
        CareerRecommendation.session_id == session.id
    ).order_by(
        CareerRecommendation.recommendation_rank
    ).all()

    return [
        serialize_recommendation(
            recommendation,
            role
        )
        for recommendation, role in rows
    ]


@router.get("/history")
def recommendation_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    sessions = db.query(RecommendationSession).filter(
        RecommendationSession.user_id == current_user.id
    ).order_by(
        RecommendationSession.id.desc()
    ).all()

    return [
        {
            "id": session.id,
            "uuid": session.uuid,
            "resume_id": session.resume_id,
            "recommendation_model": session.recommendation_model,
            "embedding_model": session.embedding_model,
            "llm_model": session.llm_model
        }
        for session in sessions
    ]


@router.get("/{recommendation_id}")
def recommendation_detail(
    recommendation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    row = db.query(
        CareerRecommendation,
        CareerRole,
        RecommendationSession
    ).join(
        CareerRole,
        CareerRole.id == CareerRecommendation.career_role_id
    ).join(
        RecommendationSession,
        RecommendationSession.id == CareerRecommendation.session_id
    ).filter(
        CareerRecommendation.id == recommendation_id,
        RecommendationSession.user_id == current_user.id
    ).first()

    if not row:

        raise HTTPException(
            status_code=404,
            detail="Recommendation not found"
        )

    recommendation, role, session = row

    return {
        **serialize_recommendation(
            recommendation,
            role
        ),
        "session_uuid": session.uuid
    }
