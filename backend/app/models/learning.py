from sqlalchemy import *

from app.core.database import Base


class LearningResource(Base):

    __tablename__ = "learning_resources"

    id = Column(
        BigInteger,
        primary_key=True
    )

    skill_id = Column(
        BigInteger,
        ForeignKey("skills.id")
    )

    title = Column(String(255))

    provider = Column(String(255))

    resource_type = Column(
        String(100)
    )

    url = Column(String(500))

    difficulty_level = Column(
        String(100)
    )

    is_free = Column(Boolean)

    rating = Column(
        DECIMAL(3,2)
    )