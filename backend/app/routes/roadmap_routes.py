from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.recommendation import RecommendationSession
from app.models.roadmap import (
    CareerRoadmap,
    RoadmapStep,
    UserRoadmapProgress
)
from app.models.user import User
from app.services.analytics_service import update_dashboard_analytics

router = APIRouter(
    prefix="/roadmaps",
    tags=["Roadmaps"]
)


class ProgressUpdateRequest(BaseModel):

    step_id: int
    status: str = "in_progress"
    completion_percentage: int = 0


class CompleteStepRequest(BaseModel):

    step_id: int


def serialize_step(
    step: RoadmapStep,
    progress: UserRoadmapProgress | None = None
) -> dict:

    return {
        "id": step.id,
        "order": step.step_order,
        "title": step.title,
        "description": step.description,
        "estimated_duration_days": step.estimated_duration_days,
        "resource_links": step.resource_links,
        "status": progress.status if progress else "not_started",
        "completion_percentage": (
            progress.completion_percentage
            if progress else 0
        )
    }


def serialize_roadmap(roadmap: CareerRoadmap) -> dict:

    return {
        "id": roadmap.id,
        "session_id": roadmap.session_id,
        "career_recommendation_id": roadmap.career_recommendation_id,
        "title": roadmap.roadmap_title,
        "content": roadmap.roadmap_content,
        "roadmap_json": roadmap.roadmap_json,
        "estimated_duration_months": roadmap.estimated_duration_months,
        "generated_by_model": roadmap.generated_by_model
    }


def get_owned_step(
    db: Session,
    user_id: int,
    step_id: int
) -> RoadmapStep | None:

    return db.query(RoadmapStep).join(
        CareerRoadmap,
        CareerRoadmap.id == RoadmapStep.roadmap_id
    ).join(
        RecommendationSession,
        RecommendationSession.id == CareerRoadmap.session_id
    ).filter(
        RoadmapStep.id == step_id,
        RecommendationSession.user_id == user_id
    ).first()


@router.get("")
def list_roadmaps(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    roadmaps = db.query(CareerRoadmap).join(
        RecommendationSession,
        RecommendationSession.id == CareerRoadmap.session_id
    ).filter(
        RecommendationSession.user_id == current_user.id
    ).order_by(
        CareerRoadmap.id.desc()
    ).all()

    return [
        serialize_roadmap(roadmap)
        for roadmap in roadmaps
    ]


@router.get("/progress")
def roadmap_progress(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    progress = db.query(UserRoadmapProgress).filter(
        UserRoadmapProgress.user_id == current_user.id
    ).all()

    return [
        {
            "id": item.id,
            "step_id": item.roadmap_step_id,
            "status": item.status,
            "completion_percentage": item.completion_percentage
        }
        for item in progress
    ]


@router.post("/progress")
def update_progress(
    payload: ProgressUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    step = get_owned_step(
        db,
        current_user.id,
        payload.step_id
    )

    if not step:

        raise HTTPException(
            status_code=404,
            detail="Roadmap step not found"
        )

    progress = db.query(UserRoadmapProgress).filter(
        UserRoadmapProgress.user_id == current_user.id,
        UserRoadmapProgress.roadmap_step_id == payload.step_id
    ).first()

    if not progress:

        progress = UserRoadmapProgress(
            user_id=current_user.id,
            roadmap_step_id=payload.step_id
        )

        db.add(progress)

    progress.status = payload.status
    progress.completion_percentage = max(
        0,
        min(
            100,
            payload.completion_percentage
        )
    )

    db.commit()
    db.refresh(progress)

    update_dashboard_analytics(
        db,
        current_user.id
    )

    return serialize_step(
        step,
        progress
    )


@router.post("/complete-step")
def complete_step(
    payload: CompleteStepRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return update_progress(
        ProgressUpdateRequest(
            step_id=payload.step_id,
            status="completed",
            completion_percentage=100
        ),
        current_user,
        db
    )


@router.get("/{roadmap_id}")
def roadmap_detail(
    roadmap_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    roadmap = db.query(CareerRoadmap).join(
        RecommendationSession,
        RecommendationSession.id == CareerRoadmap.session_id
    ).filter(
        CareerRoadmap.id == roadmap_id,
        RecommendationSession.user_id == current_user.id
    ).first()

    if not roadmap:

        raise HTTPException(
            status_code=404,
            detail="Roadmap not found"
        )

    steps = db.query(RoadmapStep).filter(
        RoadmapStep.roadmap_id == roadmap.id
    ).order_by(
        RoadmapStep.step_order
    ).all()

    progress_by_step = {
        progress.roadmap_step_id: progress
        for progress in db.query(UserRoadmapProgress).filter(
            UserRoadmapProgress.user_id == current_user.id,
            UserRoadmapProgress.roadmap_step_id.in_(
                [step.id for step in steps]
            )
        ).all()
    }

    return {
        **serialize_roadmap(roadmap),
        "steps": [
            serialize_step(
                step,
                progress_by_step.get(step.id)
            )
            for step in steps
        ]
    }
