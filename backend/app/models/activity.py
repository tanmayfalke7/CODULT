from sqlalchemy import *

from sqlalchemy.sql import func

from app.core.database import Base


class ActivityLog(Base):

    __tablename__ = "activity_logs"

    id = Column(
        BigInteger,
        primary_key=True
    )

    user_id = Column(
        BigInteger,
        ForeignKey("users.id")
    )

    activity_type = Column(
        String(255)
    )

    activity_description = Column(
        Text
    )

    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )