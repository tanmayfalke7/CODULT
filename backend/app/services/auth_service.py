import uuid

from sqlalchemy.orm import Session

from app.models.user import User

from app.core.security import (
    hash_password,
    verify_password
)


def get_user_by_email(
    db: Session,
    email: str
):

    return db.query(User).filter(
        User.email == email
    ).first()


def authenticate_user(
    db: Session,
    email: str,
    password: str
):

    user = get_user_by_email(
        db,
        email
    )

    if not user:

        return None

    if not verify_password(
        password,
        user.password_hash
    ):

        return None

    return user


def create_user(
    db: Session,
    email: str,
    password: str,
    first_name: str,
    last_name: str,
    profile_type: str
):

    existing_user = get_user_by_email(
        db,
        email
    )

    if existing_user:

        return None

    user = User(
        uuid=str(uuid.uuid4()),
        email=email,
        password_hash=hash_password(password),
        first_name=first_name,
        last_name=last_name,
        profile_type=profile_type
    )

    db.add(user)

    db.commit()

    db.refresh(user)

    return user
