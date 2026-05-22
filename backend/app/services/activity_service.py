from sqlalchemy.orm import Session

from app.models.activity import ActivityLog


def create_activity(
    db: Session,
    user_id: int,
    activity_type: str,
    activity_description: str
):

    activity = ActivityLog(
        user_id=user_id,
        activity_type=activity_type,
        activity_description=activity_description
    )

    db.add(activity)
    db.commit()
    db.refresh(activity)

    return activity
