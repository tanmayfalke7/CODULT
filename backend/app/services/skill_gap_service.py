ROLE_SKILL_MAP = {
    "ai engineer": [
        "Python",
        "Machine Learning",
        "Deep Learning",
        "NLP",
        "TensorFlow",
        "PyTorch",
        "SQL",
        "Cloud",
        "MLOps",
    ],
    "data scientist": [
        "Python",
        "Statistics",
        "Machine Learning",
        "SQL",
        "Pandas",
        "Data Visualization",
        "Feature Engineering",
        "Communication",
    ],
    "cloud architect": [
        "Cloud",
        "AWS",
        "Azure",
        "Docker",
        "Kubernetes",
        "Networking",
        "Security",
        "System Design",
    ],
    "cybersecurity analyst": [
        "Networking",
        "Linux",
        "Security",
        "SIEM",
        "Incident Response",
        "Python",
        "Risk Assessment",
    ],
    "product analyst": [
        "SQL",
        "Analytics",
        "A/B Testing",
        "Dashboards",
        "Statistics",
        "Product Thinking",
        "Communication",
    ],
    "software developer": [
        "Programming",
        "Data Structures",
        "Algorithms",
        "Databases",
        "Git",
        "APIs",
        "Testing",
    ],
}

DEFAULT_REQUIRED_SKILLS = [
    "Python",
    "SQL",
    "Problem Solving",
    "Projects",
    "Communication",
    "Git",
]


def _key(value: str) -> str:

    return value.strip().lower()


def get_required_skills(career_title: str) -> list[str]:

    title = _key(career_title or "")

    if title in ROLE_SKILL_MAP:

        return ROLE_SKILL_MAP[title]

    for role, skills in ROLE_SKILL_MAP.items():

        if role in title or title in role:

            return skills

    return DEFAULT_REQUIRED_SKILLS


def build_skill_gap_analysis(
    career_title: str,
    current_skills: list[str]
) -> dict:

    required_skills = get_required_skills(career_title)
    current_lookup = {
        _key(skill)
        for skill in current_skills
        if str(skill).strip()
    }
    matched_skills = [
        skill
        for skill in required_skills
        if _key(skill) in current_lookup
    ]
    missing_skills = [
        skill
        for skill in required_skills
        if _key(skill) not in current_lookup
    ]
    match_percentage = round(
        (len(matched_skills) / len(required_skills)) * 100,
        2
    ) if required_skills else 0

    return {
        "career": career_title,
        "required_skills": required_skills,
        "current_skills": current_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "match_percentage": match_percentage,
        "gap_percentage": round(100 - match_percentage, 2)
    }
