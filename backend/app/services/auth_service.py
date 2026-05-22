import uuid
import smtplib
from email.message import EmailMessage
from datetime import timedelta

from sqlalchemy.orm import Session

from app.core.config import (
    FRONTEND_URL,
    SMTP_FROM_EMAIL,
    SMTP_HOST,
    SMTP_PASSWORD,
    SMTP_PORT,
    SMTP_USERNAME
)
from app.models.user import User

from app.core.security import (
    create_access_token,
    decode_access_token,
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


def send_password_reset_email(
    email: str,
    reset_token: str
) -> None:

    if not SMTP_USERNAME or not SMTP_PASSWORD:

        raise RuntimeError("SMTP credentials are not configured")

    reset_url = (
        f"{FRONTEND_URL}/?reset_token={reset_token}"
    )
    message = EmailMessage()
    message["Subject"] = "Reset your CareerPilot password"
    message["From"] = SMTP_FROM_EMAIL
    message["To"] = email
    message.set_content(
        "Use this password reset link:\n\n"
        f"{reset_url}\n\n"
        "If the link does not open the reset form, copy this token into the app:\n\n"
        f"{reset_token}\n\n"
        "This link expires in 30 minutes."
    )

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:

        smtp.starttls()
        smtp.login(SMTP_USERNAME, SMTP_PASSWORD)
        smtp.send_message(message)


def create_password_reset_token(email: str) -> str:

    return create_access_token(
        f"password_reset:{email}",
        expires_delta=timedelta(minutes=30)
    )


def request_password_reset(
    db: Session,
    email: str
) -> bool:

    user = get_user_by_email(
        db,
        email
    )

    if not user:

        return False

    reset_token = create_password_reset_token(
        user.email
    )
    send_password_reset_email(
        user.email,
        reset_token
    )

    return True


def reset_password(
    db: Session,
    token: str,
    new_password: str
) -> bool:

    payload = decode_access_token(token)
    subject = payload.get("sub", "")

    if not subject.startswith("password_reset:"):

        return False

    email = subject.replace("password_reset:", "", 1)
    user = get_user_by_email(
        db,
        email
    )

    if not user:

        return False

    user.password_hash = hash_password(new_password)
    db.commit()

    return True
