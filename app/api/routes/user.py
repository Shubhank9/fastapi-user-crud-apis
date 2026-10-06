# POST /users
# GET  /users
# GET  /users/{user_id}

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse

from app.core.security import hash_password

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", response_model=UserResponse)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):

    hashed_password = hash_password(user_data.password)
    user = User(
        email=user_data.email,
        password_hash=hashed_password
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.get("/", response_model=list[UserResponse])
def get_users(
    db: Session = Depends(get_db)
):
    statement = select(User)

    result = db.execute(statement)

    users = result.scalars().all()

    return users


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    statement = select(User).where(User.id == user_id)

    result = db.execute(statement)

    user = result.scalars().first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user

