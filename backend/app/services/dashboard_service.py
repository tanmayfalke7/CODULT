from sqlalchemy.orm import Session

from app.models.resume import Resume

from app.models.recommendation import (
    CareerRecommendation,
    RecommendationSession
)

from app.models.roadmap import (
    CareerRoadmap,
    UserRoadmapProgress
)

from app.models.activity import (
    ActivityLog
)


def get_dashboard_data(
    db: Session,
    user_id: int
):

    total_resumes = db.query(
        Resume
    ).filter(
        Resume.user_id == user_id
    ).count()

    total_recommendations = db.query(
        RecommendationSession
    ).filter(
        RecommendationSession.user_id == user_id
    ).count()

    total_roadmaps = db.query(
        CareerRoadmap
    ).join(
        RecommendationSession,
        RecommendationSession.id ==
        CareerRoadmap.session_id
    ).filter(
        RecommendationSession.user_id == user_id
    ).count()

    completed_steps = db.query(
        UserRoadmapProgress
    ).filter(
        UserRoadmapProgress.user_id == user_id,
        UserRoadmapProgress.status == "completed"
    ).count()

    recent_activities = db.query(
        ActivityLog
    ).filter(
        ActivityLog.user_id == user_id
    ).order_by(
        ActivityLog.created_at.desc()
    ).limit(10).all()

    return {
        "total_resumes": total_resumes,
        "total_recommendations":
            total_recommendations,
        "total_roadmaps":
            total_roadmaps,
        "completed_steps":
            completed_steps,
        "recent_activities":
            recent_activities
    }