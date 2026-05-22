import base64
import hashlib
import hmac
import json
import os
import time
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    JWT_SECRET
)
from app.core.database import get_db
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def _b64url_encode(data: bytes) -> str:

    return base64.urlsafe_b64encode(
        data
    ).rstrip(b"=").decode("utf-8")


def _b64url_decode(data: str) -> bytes:

    padding = "=" * (-len(data) % 4)

    return base64.urlsafe_b64decode(
        data + padding
    )


def hash_password(password: str) -> str:

    salt = os.urandom(16)

    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        120000
    )

    return (
        "pbkdf2_sha256$120000$"
        f"{_b64url_encode(salt)}$"
        f"{_b64url_encode(digest)}"
    )


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:

    try:

        algorithm, iterations, salt, digest = (
            hashed_password.split("$")
        )

        if algorithm != "pbkdf2_sha256":

            return False

        calculated = hashlib.pbkdf2_hmac(
            "sha256",
            plain_password.encode("utf-8"),
            _b64url_decode(salt),
            int(iterations)
        )

        return hmac.compare_digest(
            _b64url_encode(calculated),
            digest
        )

    except Exception:

        return False


def create_access_token(
    subject: str,
    expires_delta: Optional[timedelta] = None
) -> str:

    expire_at = datetime.utcnow() + (
        expires_delta or timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    header = {
        "alg": "HS256",
        "typ": "JWT"
    }

    payload = {
        "sub": subject,
        "exp": int(expire_at.timestamp())
    }

    signing_input = ".".join([
        _b64url_encode(
            json.dumps(
                header,
                separators=(",", ":")
            ).encode("utf-8")
        ),
        _b64url_encode(
            json.dumps(
                payload,
                separators=(",", ":")
            ).encode("utf-8")
        )
    ])

    signature = hmac.new(
        JWT_SECRET.encode("utf-8"),
        signing_input.encode("utf-8"),
        hashlib.sha256
    ).digest()

    return (
        f"{signing_input}."
        f"{_b64url_encode(signature)}"
    )


def decode_access_token(token: str) -> dict:

    try:

        header, payload, signature = token.split(".")
        signing_input = f"{header}.{payload}"
        expected_signature = hmac.new(
            JWT_SECRET.encode("utf-8"),
            signing_input.encode("utf-8"),
            hashlib.sha256
        ).digest()

        if not hmac.compare_digest(
            _b64url_encode(expected_signature),
            signature
        ):

            raise ValueError("Invalid token signature")

        data = json.loads(
            _b64url_decode(payload)
        )

        if int(data.get("exp", 0)) < int(time.time()):

            raise ValueError("Token expired")

        return data

    except Exception as exc:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        ) from exc


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:

    payload = decode_access_token(token)
    user_id = payload.get("sub")

    user = db.query(User).filter(
        User.id == int(user_id)
    ).first()

    if not user or not user.is_active:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )

    return user
