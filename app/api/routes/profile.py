# POST   /profiles
# GET    /profiles
# GET    /profiles/{profile_id}
# PATCH  /profiles/{profile_id}
# DELETE /profiles/{profile_id}

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.database import get_db
from app.models.profile import Profile
from app.models.user import User
from app.schemas.profile import ProfileCreate, ProfileResponse, ProfileUpdate

router = APIRouter(
    prefix="/profiles",
    tags=["Profiles"]
)


def get_profile_or_404(profile_id: int, db: Session) -> Profile:
    statement = select(Profile).where(Profile.id == profile_id)

    profile = db.execute(statement).scalars().first()

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )

    return profile


def ensure_owner(profile: Profile, current_user: User):
    if profile.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only modify your own profile"
        )


@router.post("/", response_model=ProfileResponse, status_code=status.HTTP_201_CREATED)
def create_profile(
    profile_data: ProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    statement = select(Profile).where(Profile.user_id == current_user.id)

    if db.execute(statement).scalars().first():
        raise HTTPException(
            status_code=400,
            detail="Profile already exists for this user"
        )

    profile = Profile(
        user_id=current_user.id,
        **profile_data.model_dump()
    )

    db.add(profile)
    db.commit()
    db.refresh(profile)

    return profile


@router.get("/", response_model=list[ProfileResponse])
def get_profiles(
    db: Session = Depends(get_db)
):
    statement = select(Profile)

    return db.execute(statement).scalars().all()


@router.get("/{profile_id}", response_model=ProfileResponse)
def get_profile(
    profile_id: int,
    db: Session = Depends(get_db)
):
    return get_profile_or_404(profile_id, db)


@router.patch("/{profile_id}", response_model=ProfileResponse)
def update_profile(
    profile_id: int,
    profile_data: ProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = get_profile_or_404(profile_id, db)
    ensure_owner(profile, current_user)

    # Only update the fields the client actually sent
    for field, value in profile_data.model_dump(exclude_unset=True).items():
        setattr(profile, field, value)

    db.commit()
    db.refresh(profile)

    return profile


@router.delete("/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_profile(
    profile_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = get_profile_or_404(profile_id, db)
    ensure_owner(profile, current_user)

    db.delete(profile)
    db.commit()
