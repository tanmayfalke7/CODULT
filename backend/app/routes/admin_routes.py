from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.config import ADMIN_PASSWORD, ADMIN_USERNAME
from app.core.database import get_db
from app.core.security import create_access_token, decode_access_token
from app.models.activity import ActivityLog
from app.models.recommendation import RecommendationSession
from app.models.resume import Resume
from app.models.roadmap import CareerRoadmap
from app.models.skill import Skill
from app.models.user import User

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/admin/login"
)


class AdminLoginRequest(BaseModel):

    username: str
    password: str


def get_current_admin(
    token: str = Depends(oauth2_scheme)
) -> dict:

    payload = decode_access_token(token)
    subject = payload.get("sub", "")

    if subject != f"admin:{ADMIN_USERNAME}":

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin access required"
        )

    return {
        "username": ADMIN_USERNAME,
        "role": "admin"
    }


@router.post("/login")
def admin_login(payload: AdminLoginRequest):

    if (
        payload.username != ADMIN_USERNAME or
        payload.password != ADMIN_PASSWORD
    ):

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin username or password"
        )

    return {
        "access_token": create_access_token(
            f"admin:{ADMIN_USERNAME}"
        ),
        "token_type": "bearer",
        "admin": {
            "username": ADMIN_USERNAME,
            "role": "admin"
        }
    }


@router.get("/overview")
def admin_overview(
    admin: dict = Depends(get_current_admin),
    db: Session = Depends(get_db)
):

    recent_activities = db.query(ActivityLog).order_by(
        ActivityLog.created_at.desc()
    ).limit(8).all()

    return {
        "admin": admin,
        "stats": {
            "users": db.query(User).count(),
            "resumes": db.query(Resume).count(),
            "recommendation_sessions": db.query(RecommendationSession).count(),
            "roadmaps": db.query(CareerRoadmap).count(),
            "skills": db.query(Skill).count()
        },
        "recent_activities": [
            {
                "id": activity.id,
                "type": activity.activity_type,
                "description": activity.activity_description,
                "created_at": activity.created_at
            }
            for activity in recent_activities
        ]
    }
