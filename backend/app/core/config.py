from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./career_app.db"
)
JWT_SECRET = os.getenv(
    "JWT_SECRET",
    "change-this-secret"
)
JWT_ALGORITHM = os.getenv(
    "JWT_ALGORITHM",
    "HS256"
)
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv(
        "ACCESS_TOKEN_EXPIRE_MINUTES",
        "1440"
    )
)
SQL_ECHO = os.getenv(
    "SQL_ECHO",
    "false"
).lower() == "true"
