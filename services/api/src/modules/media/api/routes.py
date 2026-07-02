from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from src.infrastructure.auth.adapter import UserContext
from src.infrastructure.auth.dependencies import get_current_user
from src.infrastructure.database.repositories import (
    complete_media_asset,
    create_media_asset,
    get_derivatives,
    get_media_asset,
    update_media_asset_storage_key,
)
from src.infrastructure.database.session import get_db
from src.infrastructure.storage.local_storage import LocalFileStorage

MAX_BYTE_SIZE = 10 * 1024 * 1024

router = APIRouter(prefix="/media", tags=["media"])
_storage = LocalFileStorage()


@router.post("/upload-intent")
def create_upload_intent(
    body: dict,
    db: Session = Depends(get_db),
    current_user: UserContext = Depends(get_current_user),
):
    """Create an upload intent for a new media asset.

    Returns a mediaAssetId and uploadUrl for the subsequent PUT upload.
    Validates file size (max 10MB) and content type (jpeg/png/webp).
    """
    file_name: str | None = body.get("fileName")
    content_type: str | None = body.get("contentType")
    byte_size: int | None = body.get("byteSize")
    sha256: str | None = body.get("sha256")

    if not all([file_name, content_type, byte_size, sha256]):
        raise HTTPException(status_code=400, detail="Missing required fields")
    assert file_name is not None and content_type is not None
    assert byte_size is not None and sha256 is not None
    if byte_size > MAX_BYTE_SIZE:
        raise HTTPException(status_code=400, detail="File too large")
    if content_type not in {"image/jpeg", "image/png", "image/webp"}:
        raise HTTPException(status_code=400, detail="Unsupported content type")

    asset = create_media_asset(db, file_name, content_type, byte_size, sha256, owner_user_id=current_user.user_id)
    return {
        "mediaAssetId": asset.id,
        "uploadUrl": f"/media/upload/{asset.id}",
        "expiresAt": asset.created_at.isoformat(),
    }


@router.put("/upload/{media_asset_id}")
def upload_file(
    media_asset_id: str,
    file: UploadFile,
    db: Session = Depends(get_db),
    current_user: UserContext = Depends(get_current_user),
):
    """Upload a file for an existing upload intent.

    Accepts multipart file upload, saves original to local storage.
    Must be called after POST /upload-intent.
    """
    asset = get_media_asset(db, media_asset_id)
    if asset is None:
        raise HTTPException(status_code=404, detail="Media not found")

    body_bytes = file.file.read()
    _storage.save_original(media_asset_id, body_bytes)
    update_media_asset_storage_key(db, media_asset_id, f"originals/{media_asset_id}")
    return {"status": "ok", "mediaAssetId": media_asset_id}


@router.post("/complete-upload")
def complete_upload(
    body: dict,
    db: Session = Depends(get_db),
    current_user: UserContext = Depends(get_current_user),
):
    """Complete an upload intent and generate derivative stubs.

    Confirms SHA256 match, marks asset as ready, and generates
    thumbnail and public derivative stubs on disk.
    """
    sha256 = body.get("sha256")
    if not sha256:
        raise HTTPException(status_code=400, detail="Missing sha256")

    media_asset_id = body.get("mediaAssetId")
    if not media_asset_id:
        raise HTTPException(status_code=400, detail="Missing mediaAssetId")

    asset = complete_media_asset(db, media_asset_id, sha256)
    if asset is None:
        raise HTTPException(status_code=404, detail="Upload intent not found or SHA mismatch")

    try:
        deriv_urls = _storage.generate_derivative_stubs(media_asset_id)
    except FileNotFoundError:
        deriv_urls = {"thumbnail": None, "public": None}  # type: ignore[dict-item]

    return {
        "status": "ok",
        "mediaAssetId": media_asset_id,
        "derivatives": {
            "thumbnailUrl": deriv_urls.get("thumbnail"),
            "derivativeUrl": deriv_urls.get("public"),
            "exifStripped": True,
        },
    }


@router.get("/derivatives/{media_asset_id}")
def get_media_derivatives(
    media_asset_id: str,
    db: Session = Depends(get_db),
    current_user: UserContext = Depends(get_current_user),
):
    """Get derivative URLs (thumbnail + public) for a media asset.

    Returns paths suitable for use with GET /media/files/{subdir}/{filename}.
    """
    asset = get_media_asset(db, media_asset_id)
    if asset is None:
        raise HTTPException(status_code=404, detail="Media not found")

    derivs = get_derivatives(db, media_asset_id)
    thumb_path = None
    pub_path = None
    for d in derivs:
        if d.size_label == "thumbnail":
            thumb_path = f"/v1/media/files/thumbs/{media_asset_id}.webp"
        elif d.size_label == "public":
            pub_path = f"/v1/media/files/public/{media_asset_id}.webp"

    return {
        "thumbnailUrl": thumb_path,
        "derivativeUrl": pub_path,
        "exifStripped": True,
    }


@router.get("/files/{subdir:path}/{filename}")
def serve_file(subdir: str, filename: str):
    """Serve a stored file (original, thumbnail, or public derivative).

    Public endpoint (no auth required). Subdir must be one of
    originals/, thumbs/, or public/.
    """
    path = _storage.get_path(f"{subdir}/{filename}")
    if path is None:
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path=path)
