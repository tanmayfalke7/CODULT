import json
import os
import shutil
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services.analytics_service import update_dashboard_analytics
from app.services.parser import (
    extract_text_from_docx,
    extract_text_from_pdf
)
from app.services.recommendation_service import (
    create_recommendation_session,
    save_career_recommendations
)
from app.services.resume_service import save_resume
from app.services.roadmap_service import save_career_roadmap
from app.services.skill_service import save_user_skills

router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)

TEMP_DIR = Path("app/temp")
TEMP_DIR.mkdir(
    parents=True,
    exist_ok=True
)


def _normalize_skills(value) -> list[str]:

    if isinstance(value, list):

        return [
            str(skill).strip()
            for skill in value
            if str(skill).strip()
        ]

    if not value:

        return []

    return [
        skill.strip()
        for skill in str(value).split(",")
        if skill.strip()
    ]


def _extract_text(file_path: Path, extension: str) -> str:

    if extension == ".pdf":

        return extract_text_from_pdf(
            str(file_path)
        )

    if extension == ".docx":

        return extract_text_from_docx(
            str(file_path)
        )

    if extension == ".txt":

        return file_path.read_text(
            encoding="utf-8",
            errors="ignore"
        )

    raise HTTPException(
        status_code=400,
        detail="Unsupported file format. Upload PDF, DOCX, or TXT."
    )


def _roadmap_to_json(roadmap_text: str) -> dict:

    try:

        parsed = json.loads(roadmap_text)

        if isinstance(parsed, dict):

            return parsed

    except Exception:

        pass

    default_steps = [
        "Foundation Skills",
        "Core Tools",
        "Portfolio Projects",
        "Certifications",
        "Interview Preparation",
        "Career Growth"
    ]

    return {
        "summary": roadmap_text,
        "steps": [
            {
                "title": title,
                "description": f"Work through the {title.lower()} phase for this career path.",
                "duration_days": 30,
                "resources": []
            }
            for title in default_steps
        ]
    }


@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    from app.services.llm_extractor import extract_resume_details
    from app.services.predictor import predict_career
    from app.services.roadmap_generator import generate_roadmap

    original_name = file.filename or "resume"
    extension = Path(original_name).suffix.lower()
    file_path = TEMP_DIR / original_name

    with file_path.open("wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    resume_text = _extract_text(
        file_path,
        extension
    )

    user_data = extract_resume_details(
        resume_text
    )

    resume = save_resume(
        db=db,
        user_id=current_user.id,
        title=os.path.splitext(original_name)[0],
        original_file_name=original_name,
        file_url=str(file_path),
        extracted_text=resume_text,
        extracted_json=user_data,
        file_type=extension.replace(".", "")
    )

    skills = save_user_skills(
        db=db,
        user_id=current_user.id,
        resume_id=resume.id,
        skills=_normalize_skills(
            user_data.get("skills")
        )
    )

    prediction_result = predict_career(
        user_data
    )

    recommendation_session = create_recommendation_session(
        db=db,
        user_id=current_user.id,
        resume_id=resume.id
    )

    saved_recommendations = save_career_recommendations(
        db=db,
        session_id=recommendation_session.id,
        recommendations=prediction_result["top_matches"],
        user_id=current_user.id
    )

    predicted_career = prediction_result[
        "predicted_career"
    ]

    roadmap_text = generate_roadmap(
        predicted_career,
        user_data
    )

    roadmap_json = _roadmap_to_json(
        roadmap_text
    )

    roadmap = save_career_roadmap(
        db=db,
        session_id=recommendation_session.id,
        recommendation_id=saved_recommendations[0].id,
        roadmap_title=f"{predicted_career} Roadmap",
        roadmap_content=roadmap_text,
        roadmap_json=roadmap_json,
        user_id=current_user.id
    )

    analytics = update_dashboard_analytics(
        db=db,
        user_id=current_user.id
    )

    return {
        "success": True,
        "resume": {
            "id": resume.id,
            "uuid": resume.uuid,
            "file_name": resume.original_file_name,
            "uploaded_at": resume.uploaded_at
        },
        "extracted_user_data": user_data,
        "saved_skills": skills,
        "recommended_career": predicted_career,
        "top_career_matches": prediction_result["top_matches"],
        "recommendation_session_id": recommendation_session.id,
        "roadmap": {
            "id": roadmap.id,
            "title": roadmap.roadmap_title,
            "content": roadmap.roadmap_content,
            "steps": roadmap_json.get("steps", [])
        },
        "analytics": {
            "total_resumes": analytics.total_resumes_uploaded,
            "total_recommendations": analytics.total_recommendations_generated,
            "completed_steps": analytics.completed_roadmap_steps
        }
    }
