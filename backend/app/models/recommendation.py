# from sqlalchemy import Column
# from sqlalchemy import String
# from sqlalchemy import ForeignKey
# from sqlalchemy import BigInteger
# from sqlalchemy import DECIMAL
# from sqlalchemy import TIMESTAMP
# from sqlalchemy import Text

# from sqlalchemy.sql import func

# from app.core.database import Base


# class RecommendationSession(Base):

#     __tablename__ = "recommendation_sessions"

#     id = Column(
#         BigInteger,
#         primary_key=True,
#         index=True
#     )

#     uuid = Column(
#         String(36),
#         unique=True
#     )

#     user_id = Column(
#         BigInteger,
#         ForeignKey("users.id")
#     )

#     resume_id = Column(
#         BigInteger,
#         ForeignKey("resumes.id")
#     )

#     recommendation_model = Column(
#         String(255)
#     )

#     embedding_model = Column(
#         String(255)
#     )

#     llm_model = Column(
#         String(255)
#     )

#     generated_at = Column(
#         TIMESTAMP,
#         server_default=func.now()
#     )


# class CareerRecommendation(Base):

#     __tablename__ = "career_recommendations"

#     id = Column(
#         BigInteger,
#         primary_key=True,
#         index=True
#     )

#     session_id = Column(
#         BigInteger,
#         ForeignKey(
#             "recommendation_sessions.id"
#         )
#     )

#     career_title = Column(
#         String(255)
#     )

#     match_score = Column(
#         DECIMAL(5,2)
#     )

#     recommendation_reason = Column(
#         Text
#     )

#     created_at = Column(
#         TIMESTAMP,
#         server_default=func.now()
#     )
from sqlalchemy import *

from app.core.database import Base


class RecommendationSession(Base):

    __tablename__ = "recommendation_sessions"

    id = Column(
        BigInteger,
        primary_key=True
    )

    uuid = Column(
        String(36),
        unique=True
    )

    user_id = Column(
        BigInteger,
        ForeignKey("users.id")
    )

    resume_id = Column(
        BigInteger,
        ForeignKey("resumes.id")
    )

    recommendation_model = Column(
        String(255)
    )

    embedding_model = Column(
        String(255)
    )

    llm_model = Column(
        String(255)
    )


class CareerRecommendation(Base):

    __tablename__ = "career_recommendations"

    id = Column(
        BigInteger,
        primary_key=True
    )

    session_id = Column(
        BigInteger,
        ForeignKey(
            "recommendation_sessions.id"
        )
    )

    career_role_id = Column(
        BigInteger,
        ForeignKey(
            "career_roles.id"
        )
    )

    recommendation_rank = Column(
        Integer
    )

    match_score = Column(
        DECIMAL(5,2)
    )

    recommendation_reason = Column(
        Text
    )