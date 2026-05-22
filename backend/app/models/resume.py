from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Enum
from sqlalchemy import TIMESTAMP
from sqlalchemy import ForeignKey
from sqlalchemy import BigInteger
from sqlalchemy import JSON
from sqlalchemy import Text

from sqlalchemy.sql import func

from app.core.database import Base


class Resume(Base):

    __tablename__ = "resumes"

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

    user_id = Column(
        BigInteger,
        ForeignKey("users.id")
    )

    title = Column(
        String(255)
    )

    original_file_name = Column(
        String(255)
    )

    file_url = Column(
        String(500)
    )

    extracted_text = Column(
        Text
    )

    extracted_json = Column(
        JSON
    )

    file_type = Column(
        Enum(
            "pdf",
            "docx",
            "txt",
            name="file_type_enum"
        )
    )

    uploaded_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )