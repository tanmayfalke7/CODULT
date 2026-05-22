from sqlalchemy.orm import Session

from app.models.analytics import (
    DashboardAnalytics
)

from app.models.resume import Resume

from app.models.recommendation import (
    RecommendationSession
)

from app.models.roadmap import (
    UserRoadmapProgress
)


def update_dashboard_analytics(
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

    completed_steps = db.query(
        UserRoadmapProgress
    ).filter(
        UserRoadmapProgress.user_id == user_id,
        UserRoadmapProgress.status == "completed"
    ).count()

    analytics = db.query(
        DashboardAnalytics
    ).filter(
        DashboardAnalytics.user_id ==
        user_id
    ).first()

    if not analytics:

        analytics = DashboardAnalytics(
            user_id=user_id
        )

        db.add(analytics)

    analytics.total_resumes_uploaded = (
        total_resumes
    )

    analytics.total_recommendations_generated = (
        total_recommendations
    )

    analytics.completed_roadmap_steps = (
        completed_steps
    )

    db.commit()

    db.refresh(analytics)

    return analytics