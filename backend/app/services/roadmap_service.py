import json

from sqlalchemy.orm import Session

from app.models.roadmap import (
    CareerRoadmap,
    RoadmapStep
)

from app.services.activity_service import (
    create_activity
)


def save_career_roadmap(
    db: Session,
    session_id: int,
    recommendation_id: int,
    roadmap_title: str,
    roadmap_content: str,
    roadmap_json: dict,
    user_id: int
):

    roadmap = CareerRoadmap(
        session_id=session_id,
        career_recommendation_id=recommendation_id,
        roadmap_title=roadmap_title,
        roadmap_content=roadmap_content,
        roadmap_json=roadmap_json,
        estimated_duration_months=6,
        generated_by_model="llama3-70b-8192"
    )

    db.add(roadmap)

    db.commit()

    db.refresh(roadmap)

    # Save roadmap steps
    if "steps" in roadmap_json:

        for index, step in enumerate(
            roadmap_json["steps"]
        ):

            roadmap_step = RoadmapStep(
                roadmap_id=roadmap.id,
                step_order=index + 1,
                title=step.get(
                    "title",
                    "Untitled Step"
                ),
                description=step.get(
                    "description",
                    ""
                ),
                estimated_duration_days=step.get(
                    "duration_days",
                    7
                ),
                resource_links=step.get(
                    "resources",
                    []
                )
            )

            db.add(roadmap_step)

    db.commit()

    create_activity(
        db=db,
        user_id=user_id,
        activity_type="roadmap_generated",
        activity_description=f"""
        Generated roadmap:
        {roadmap_title}
        """
    )

    return roadmap