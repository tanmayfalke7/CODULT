from groq import Groq

from app.core.config import GROQ_API_KEY

client = Groq(
    api_key=GROQ_API_KEY
)


def generate_roadmap(career, user_data):

    prompt = f"""
    User Profile:
    {user_data}

    Recommended Career:
    {career}

    Create a detailed roadmap.

    Include:
    1. Required Skills
    2. Learning Path
    3. Certifications
    4. Project Ideas
    5. Interview Preparation
    6. Career Growth
    7. Salary Insights
    8. 6-Month Plan

    Return structured response.
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
            temperature=0.5
        )

        return response.choices[0].message.content

    except Exception:

        return f"""
        6-Month Roadmap for {career}

        Month 1: Strengthen foundations and revise core concepts.
        Month 2: Learn role-specific tools and workflows.
        Month 3: Build one guided portfolio project.
        Month 4: Build one independent capstone project.
        Month 5: Prepare certifications and interview topics.
        Month 6: Apply to internships or jobs with a polished portfolio.
        """
