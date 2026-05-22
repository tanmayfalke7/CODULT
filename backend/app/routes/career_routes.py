from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File

import os
import shutil

from app.services.parser import (
    extract_text_from_pdf,
    extract_text_from_docx
)

router = APIRouter()

TEMP_DIR = "app/temp"

os.makedirs(
    TEMP_DIR,
    exist_ok=True
)


@router.post("/recommend-career")
async def recommend_career(
    file: UploadFile = File(...)
):

    from app.services.llm_extractor import (
        extract_resume_details
    )
    from app.services.predictor import (
        predict_career
    )
    from app.services.roadmap_generator import (
        generate_roadmap
    )

    file_path = f"{TEMP_DIR}/{file.filename}"

    with open(file_path, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    # Extract resume text
    if file.filename.endswith(".pdf"):

        resume_text = extract_text_from_pdf(
            file_path
        )

    elif file.filename.endswith(".docx"):

        resume_text = extract_text_from_docx(
            file_path
        )

    else:

        return {
            "error": "Unsupported file format"
        }

    # Extract structured user data
    user_data = extract_resume_details(
        resume_text
    )

    # Predict career
    prediction_result = predict_career(
        user_data
    )

    predicted_career = prediction_result[
        "predicted_career"
    ]

    # Generate roadmap
    roadmap = generate_roadmap(
        predicted_career,
        user_data
    )

    return {
        "success": True,
        "extracted_user_data": user_data,
        "recommended_career": predicted_career,
        "top_career_matches": prediction_result[
            "top_matches"
        ],
        "roadmap": roadmap
    }
