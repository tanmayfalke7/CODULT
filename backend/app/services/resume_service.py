import uuid

from sqlalchemy.orm import Session

from app.models.resume import Resume

from app.services.activity_service import (
    create_activity
)


def save_resume(
    db: Session,
    user_id: int,
    title: str,
    original_file_name: str,
    file_url: str,
    extracted_text: str,
    extracted_json: dict,
    file_type: str
):

    resume = Resume(
        uuid=str(uuid.uuid4()),
        user_id=user_id,
        title=title,
        original_file_name=original_file_name,
        file_url=file_url,
        extracted_text=extracted_text,
        extracted_json=extracted_json,
        file_type=file_type
    )

    db.add(resume)

    db.commit()

    db.refresh(resume)

    create_activity(
        db=db,
        user_id=user_id,
        activity_type="resume_upload",
        activity_description=f"Uploaded resume: {title}"
    )

    return resume
