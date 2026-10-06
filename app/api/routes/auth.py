# POST /auth/login

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.schemas.auth import UserLogin
from app.core.security import verify_password, create_access_token


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/login")
def login(
    response: Response,
    user_data: UserLogin,
    db: Session = Depends(get_db)
):
    statement = select(User).where(User.email == user_data.email)

    result = db.execute(statement)

    user = result.scalars().first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    is_password_valid = verify_password(
        user_data.password,
        user.password_hash
    )

    if not is_password_valid:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(user.id)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=30 * 60
    )

    return {
        "message": "Login successful"
    }