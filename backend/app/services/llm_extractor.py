import json

from groq import Groq

from app.core.config import GROQ_API_KEY

client = Groq(
    api_key=GROQ_API_KEY
)


def extract_resume_details(resume_text):

    prompt = f"""
    Analyze this resume carefully.

    Extract:
    1. Skills
    2. Interests
    3. Education
    4. Experience Level
    5. Certifications

    Return ONLY valid JSON.

    Example:

    {{
        "skills": "Python, SQL, Machine Learning",
        "interests": "AI, Data Science",
        "education": "B.Tech Computer Science",
        "experience_level": "Fresher",
        "certifications": "AWS Cloud Practitioner"
    }}

    Resume:
    {resume_text}
    """

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        content = response.choices[0].message.content

    except Exception:

        return _fallback_extract(
            resume_text
        )

    try:

        data = json.loads(content)

        return data

    except Exception:

        return _fallback_extract(
            resume_text
        )


def _fallback_extract(resume_text: str):

    known_skills = [
        "Python",
        "SQL",
        "Machine Learning",
        "Data Science",
        "React",
        "FastAPI",
        "Cloud",
        "AWS",
        "Cybersecurity",
        "NLP"
    ]

    text = resume_text.lower()
    skills = [
        skill
        for skill in known_skills
        if skill.lower() in text
    ]

    return {
        "skills": ", ".join(skills) or "Python, SQL, Machine Learning",
        "interests": "AI, Data Science",
        "education": "Not specified",
        "experience_level": "Fresher",
        "certifications": ""
    }
