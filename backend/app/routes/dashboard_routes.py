from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.activity import ActivityLog
from app.models.recommendation import RecommendationSession
from app.models.resume import Resume
from app.models.roadmap import CareerRoadmap, UserRoadmapProgress
from app.models.user import User
from app.services.dashboard_service import get_dashboard_data

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


def serialize_activity(activity: ActivityLog) -> dict:

    return {
        "id": activity.id,
        "type": activity.activity_type,
        "description": activity.activity_description,
        "created_at": activity.created_at
    }


@router.get("")
def dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    data = get_dashboard_data(
        db,
        current_user.id
    )

    return {
        **data,
        "recent_activities": [
            serialize_activity(activity)
            for activity in data["recent_activities"]
        ]
    }


@router.get("/history")
def history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    resumes = db.query(Resume).filter(
        Resume.user_id == current_user.id
    ).order_by(
        Resume.uploaded_at.desc()
    ).all()

    return [
        {
            "id": resume.id,
            "uuid": resume.uuid,
            "title": resume.title,
            "file_name": resume.original_file_name,
            "uploaded_at": resume.uploaded_at
        }
        for resume in resumes
    ]


@router.get("/activities")
def activities(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    records = db.query(ActivityLog).filter(
        ActivityLog.user_id == current_user.id
    ).order_by(
        ActivityLog.created_at.desc()
    ).limit(50).all()

    return [
        serialize_activity(activity)
        for activity in records
    ]


@router.get("/stats")
def stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    total_resumes = db.query(Resume).filter(
        Resume.user_id == current_user.id
    ).count()

    total_roadmaps = db.query(CareerRoadmap).join(
        RecommendationSession,
        RecommendationSession.id == CareerRoadmap.session_id
    ).filter(
        RecommendationSession.user_id == current_user.id
    ).count()

    completed_steps = db.query(UserRoadmapProgress).filter(
        UserRoadmapProgress.user_id == current_user.id,
        UserRoadmapProgress.status == "completed"
    ).count()

    return {
        "total_resumes": total_resumes,
        "total_roadmaps": total_roadmaps,
        "completed_steps": completed_steps
    }
