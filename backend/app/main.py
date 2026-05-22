from fastapi import FastAPI

from app.core.database import (
    engine as db_engine,
    Base
)

from fastapi.middleware.cors import (
    CORSMiddleware
)

from app.routes.career_routes import (
    router
)
from app.routes.auth_routes import (
    router as auth_router
)
from app.routes.admin_routes import (
    router as admin_router
)
from app.routes.dashboard_routes import (
    router as dashboard_router
)
from app.routes.recommendation_routes import (
    router as recommendation_router
)
from app.routes.resume_routes import (
    router as resume_router
)
from app.routes.roadmap_routes import (
    router as roadmap_router
)
from app.routes.skill_routes import (
    router as skill_router
)

# Import models
from app.models.user import User
from app.models.resume import Resume
from app.models.recommendation import (
    RecommendationSession,
    CareerRecommendation
)
from app.models.roadmap import (
    CareerRoadmap
)
from app.models.skill import Skill
from app.models.user import *
from app.models.profile import *
from app.models.resume import *
from app.models.skill import *
from app.models.career import *
from app.models.recommendation import *
from app.models.roadmap import *
from app.models.learning import *
from app.models.analytics import *
from app.models.activity import *
# Create tables
Base.metadata.create_all(
    bind=db_engine
)

app = FastAPI(
    title="AI Career Recommendation API",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router)
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(resume_router)
app.include_router(dashboard_router)
app.include_router(roadmap_router)
app.include_router(recommendation_router)
app.include_router(skill_router)


@app.get("/")
def home():

    return {
        "message": "AI Career Recommendation API Running"
    }
