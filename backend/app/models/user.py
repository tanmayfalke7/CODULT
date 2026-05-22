from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import Enum
from sqlalchemy import TIMESTAMP
from sqlalchemy import BigInteger

from sqlalchemy.sql import func
from app.core.database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(
        BigInteger,
        primary_key=True,
        index=True
    )

    uuid = Column(
        String(36),
        unique=True,
        nullable=False
    )

    email = Column(
        String(255),
        unique=True,
        nullable=False
    )

    password_hash = Column(
        String(255),
        nullable=False
    )

    first_name = Column(
        String(100)
    )

    last_name = Column(
        String(100)
    )

    profile_type = Column(
        Enum(
            "school_student",
            "tenth_passout",
            "engineering_student",
            "college_student",
            "working_professional",
            "career_switcher",
            name="profile_type_enum"
        ),
        nullable=False
    )

    role = Column(
        Enum(
            "user",
            "admin",
            name="role_enum"
        ),
        default="user"
    )

    is_active = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )
