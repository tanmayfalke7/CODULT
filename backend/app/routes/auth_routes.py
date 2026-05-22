from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import (
    create_access_token,
    get_current_user
)
from app.models.user import User
from app.services.auth_service import (
    authenticate_user,
    create_user
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


class RegisterRequest(BaseModel):

    email: str
    password: str
    first_name: str | None = None
    last_name: str | None = None
    profile_type: str


class LoginRequest(BaseModel):

    email: str
    password: str


def serialize_user(user: User) -> dict:

    return {
        "id": user.id,
        "uuid": user.uuid,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "profile_type": user.profile_type,
        "role": user.role,
        "is_active": user.is_active,
        "created_at": user.created_at
    }


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(
    payload: RegisterRequest,
    db: Session = Depends(get_db)
):

    user = create_user(
        db=db,
        email=payload.email,
        password=payload.password,
        first_name=payload.first_name,
        last_name=payload.last_name,
        profile_type=payload.profile_type
    )

    if not user:

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    access_token = create_access_token(
        str(user.id)
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": serialize_user(user)
    }


@router.post("/login")
def login(
    payload: LoginRequest,
    db: Session = Depends(get_db)
):

    user = authenticate_user(
        db=db,
        email=payload.email,
        password=payload.password
    )

    if not user:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    return {
        "access_token": create_access_token(
            str(user.id)
        ),
        "token_type": "bearer",
        "user": serialize_user(user)
    }


@router.get("/me")
def me(
    current_user: User = Depends(get_current_user)
):

    return serialize_user(current_user)
