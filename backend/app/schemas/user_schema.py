from pydantic import BaseModel
from typing import Optional


class UserCreate(BaseModel):

    email: str

    password: str

    first_name: Optional[str]

    last_name: Optional[str]

    profile_type: str