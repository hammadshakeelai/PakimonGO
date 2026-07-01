import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from ..models import MediaAsset, MediaDerivative


def create_media_asset(
    db: Session,
    file_name: str,
    content_type: str,
    byte_size: int,
    sha256: str,
    owner_user_id: str | None = None,
) -> MediaAsset:
    media_asset_id = f"media_{uuid.uuid4().hex[:24]}"
    asset = MediaAsset(
        id=media_asset_id,
        owner_user_id=owner_user_id,
        file_name=file_name,
        content_type=content_type,
        byte_size=byte_size,
        sha256=sha256,
        storage_key=f"originals/{media_asset_id}",
        processing_state="pending",
    )
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset


def get_media_asset(db: Session, media_asset_id: str) -> MediaAsset | None:
    return db.query(MediaAsset).filter(MediaAsset.id == media_asset_id).first()


def update_media_asset_storage_key(db: Session, media_asset_id: str, storage_key: str) -> MediaAsset | None:
    asset = get_media_asset(db, media_asset_id)
    if asset is None:
        return None
    asset.storage_key = storage_key
    asset.processing_state = "uploaded"
    asset.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(asset)
    return asset


def complete_media_asset(db: Session, media_asset_id: str, sha256: str) -> MediaAsset | None:
    asset = get_media_asset(db, media_asset_id)
    if asset is None or asset.sha256 != sha256:
        return None
    asset.processing_state = "ready"
    asset.updated_at = datetime.now(timezone.utc)

    deriv = MediaDerivative(
        media_asset_id=media_asset_id,
        size_label="thumbnail",
        storage_key=f"thumbs/{media_asset_id}.webp",
        exif_stripped=True,
        visibility_state="public",
    )
    db.add(deriv)

    deriv_public = MediaDerivative(
        media_asset_id=media_asset_id,
        size_label="public",
        storage_key=f"public/{media_asset_id}.webp",
        exif_stripped=True,
        visibility_state="public",
    )
    db.add(deriv_public)

    db.commit()
    db.refresh(asset)
    return asset


def get_derivatives(db: Session, media_asset_id: str) -> list[MediaDerivative]:
    return (
        db.query(MediaDerivative)
        .filter(MediaDerivative.media_asset_id == media_asset_id)
        .all()
    )
