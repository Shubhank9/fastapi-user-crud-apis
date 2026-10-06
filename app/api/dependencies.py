from typing import Optional

from fastapi import Cookie, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import verify_access_token
from app.db.database import get_db
from app.models.user import User


def get_current_user(
    access_token: Optional[str] = Cookie(default=None),
    db: Session = Depends(get_db)
):
    if not access_token:
        raise HTTPException(
            status_code=401,
            detail="Authentication required"
        )

    try:
        payload = verify_access_token(access_token)  # Verify the access token and extract the payload
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    user_id = payload.get("sub")   # Extract user ID from the token payload

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    statement = select(User).where(User.id == int(user_id))

    result = db.execute(statement)

    user = result.scalars().first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user