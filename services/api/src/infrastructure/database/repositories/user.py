from datetime import datetime, timezone

from sqlalchemy.orm import Session

from ..models import User


def get_or_create_user(db: Session, user_id: str) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        user = User(id=user_id)
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


def update_user(db: Session, user_id: str, age_band: str | None = None, home_region: str | None = None) -> User | None:
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        return None
    if age_band is not None:
        user.age_band = age_band
    if home_region is not None:
        user.home_region = home_region
    user.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(user)
    return user
