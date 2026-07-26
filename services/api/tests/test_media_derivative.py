import io
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from PIL import Image
from src.main import app

client = TestClient(app)
AUTH_HEADER = {"Authorization": "Bearer test_token_valid"}

SAMPLE_SHA = "a" * 64


def _real_jpeg_bytes() -> bytes:
    """A genuinely Pillow-decodable JPEG (unlike a hand-rolled magic-byte
    stub) so derivative generation exercises the real re-encode path."""
    buf = io.BytesIO()
    Image.new("RGB", (32, 32), color=(120, 160, 90)).save(buf, "JPEG")
    return buf.getvalue()


def _create_upload_intent():
    resp = client.post("/v1/media/upload-intent", json={
        "fileName": "sparrow.jpg",
        "contentType": "image/jpeg",
        "byteSize": 500000,
        "sha256": SAMPLE_SHA,
    }, headers=AUTH_HEADER)
    return resp.json()["mediaAssetId"]


def _upload_file(media_asset_id: str):
    client.put(
        f"/v1/media/upload/{media_asset_id}",
        files={"file": ("test.jpg", _real_jpeg_bytes(), "image/jpeg")},
        headers=AUTH_HEADER,
    )


def _create_and_complete_upload():
    media_asset_id = _create_upload_intent()
    _upload_file(media_asset_id)
    client.post("/v1/media/complete-upload", json={
        "mediaAssetId": media_asset_id,
        "sha256": SAMPLE_SHA,
    }, headers=AUTH_HEADER)
    return media_asset_id


def test_complete_upload_returns_derivatives():
    media_asset_id = _create_upload_intent()
    _upload_file(media_asset_id)
    resp = client.post("/v1/media/complete-upload", json={
        "mediaAssetId": media_asset_id,
        "sha256": SAMPLE_SHA,
    }, headers=AUTH_HEADER)
    data = resp.json()
    assert "derivatives" in data
    assert "thumbnailUrl" in data["derivatives"]
    assert "derivativeUrl" in data["derivatives"]
    assert data["derivatives"]["exifStripped"] is True
    assert data["derivatives"]["thumbnailUrl"].startswith("/v1/media/files/thumbs")
    assert data["derivatives"]["derivativeUrl"].startswith("/v1/media/files/public")


def test_get_derivatives():
    media_asset_id = _create_and_complete_upload()
    resp = client.get(f"/v1/media/derivatives/{media_asset_id}", headers=AUTH_HEADER)
    assert resp.status_code == 200
    data = resp.json()
    assert data["exifStripped"] is True
    assert "thumbnailUrl" in data
    assert "derivativeUrl" in data


def test_get_derivatives_not_found():
    resp = client.get("/v1/media/derivatives/media_nonexistent", headers=AUTH_HEADER)
    assert resp.status_code == 404


def test_derivatives_no_original_url():
    media_asset_id = _create_and_complete_upload()
    resp = client.get(f"/v1/media/derivatives/{media_asset_id}", headers=AUTH_HEADER)
    data = resp.json()
    assert "originalUrl" not in data
    assert "storagePath" not in data
    assert "signedUrl" not in data


def test_derivative_url_separate_namespace():
    media_asset_id = _create_and_complete_upload()
    resp = client.get(f"/v1/media/derivatives/{media_asset_id}", headers=AUTH_HEADER)
    data = resp.json()
    assert "/public/" in data["derivativeUrl"]
    assert "/thumbs/" in data["thumbnailUrl"]
    assert "/original/" not in data["derivativeUrl"]


def test_original_file_is_not_publicly_servable():
    """The original may carry EXIF (e.g. phone GPS); mediaAssetId is public
    (profiles/feed expose it), so serving originals/ over this unauthenticated
    route would let anyone undo the derivative's metadata stripping."""
    media_asset_id = _create_and_complete_upload()
    resp = client.get(f"/v1/media/files/originals/{media_asset_id}")
    assert resp.status_code == 404


def test_derivatives_still_served_from_allowed_subdirs():
    media_asset_id = _create_and_complete_upload()
    thumb = client.get(f"/v1/media/files/thumbs/{media_asset_id}.webp")
    public = client.get(f"/v1/media/files/public/{media_asset_id}.webp")
    assert thumb.status_code == 200
    assert public.status_code == 200


def test_undecodable_upload_gets_no_derivative_and_honest_exif_flag():
    """A file that passes the shallow magic-byte sniff but that Pillow can't
    actually decode must not silently fall back to copying the raw bytes
    (that used to leak whatever metadata the "original" carried, mislabeled
    as a stripped derivative)."""
    media_asset_id = _create_upload_intent()
    client.put(
        f"/v1/media/upload/{media_asset_id}",
        files={"file": (
            "fake.jpg",
            b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01" + b"\x00" * 64,
            "image/jpeg",
        )},
        headers=AUTH_HEADER,
    )
    resp = client.post("/v1/media/complete-upload", json={
        "mediaAssetId": media_asset_id,
        "sha256": SAMPLE_SHA,
    }, headers=AUTH_HEADER)
    data = resp.json()
    assert data["derivatives"]["exifStripped"] is False
    assert data["derivatives"]["thumbnailUrl"] is None
    assert data["derivatives"]["derivativeUrl"] is None
