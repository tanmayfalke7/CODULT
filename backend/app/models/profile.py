from sqlalchemy import *

from sqlalchemy.orm import relationship

from app.core.database import Base


class UserProfile(Base):

    __tablename__ = "user_profiles"

    id = Column(
        BigInteger,
        primary_key=True
    )

    user_id = Column(
        BigInteger,
        ForeignKey("users.id")
    )

    headline = Column(String(255))

    bio = Column(Text)

    location = Column(String(255))

    current_education = Column(
        String(255)
    )

    current_job_title = Column(
        String(255)
    )

    years_of_experience = Column(
        Integer,
        default=0
    )

    preferred_career_domains = Column(
        JSON
    )

    career_goals = Column(Text)

    profile_completeness = Column(
        Integer,
        default=0
    )

    user = relationship(
        "User",
        backref="profile"
    )
