import os
import shutil
from pathlib import Path

from src.infrastructure.storage.base import StorageProvider

UPLOAD_BASE = Path(os.getenv("UPLOAD_BASE", "data/uploads"))

_HAS_PIL = False
try:
    from PIL import Image
    _HAS_PIL = True
except ImportError:
    Image = None  # type: ignore[assignment]


class LocalFileStorage(StorageProvider):
    def __init__(self, base_dir: Path | None = None):
        self._base = base_dir or UPLOAD_BASE
        for sub in ("originals", "thumbs", "public"):
            (self._base / sub).mkdir(parents=True, exist_ok=True)

    def save_original(self, asset_id: str, content: bytes) -> str:
        path = self._original_path(asset_id)
        path.write_bytes(content)
        return str(path)

    def get_url(self, key: str) -> str | None:
        return None

    def read_original(self, asset_id: str) -> bytes | None:
        path = self._original_path(asset_id)
        return path.read_bytes() if path.exists() else None

    def generate_derivative_stubs(self, asset_id: str) -> dict[str, str]:
        original = self._original_path(asset_id)
        if not original.exists():
            raise FileNotFoundError(f"Original not found for {asset_id}")

        try:
            if _HAS_PIL:
                img = Image.open(original)
                _sizes = [
                    ("thumbnail", self._thumb_path(asset_id), (200, 200)),
                    ("public", self._public_path(asset_id), (800, 800)),
                ]
                for label, dest, size in _sizes:
                    resized = img.copy()
                    resized.thumbnail(size, Image.LANCZOS)  # type: ignore[attr-defined]
                    resized.save(dest, "WEBP", quality=85)
            else:
                for dest in [self._thumb_path(asset_id), self._public_path(asset_id)]:
                    shutil.copy2(original, dest)
        except Exception:
            for dest in [self._thumb_path(asset_id), self._public_path(asset_id)]:
                shutil.copy2(original, dest)

        return {
            "thumbnail": f"/v1/media/files/thumbs/{asset_id}.webp",
            "public": f"/v1/media/files/public/{asset_id}.webp",
        }

    def delete_all(self, asset_id: str):
        for path in [self._original_path(asset_id), self._thumb_path(asset_id), self._public_path(asset_id)]:
            if path.exists():
                path.unlink()

    def get_path(self, relative: str) -> Path | None:
        full = (self._base / relative).resolve()
        if full.exists() and str(full).startswith(str(self._base.resolve())):
            return full
        return None

    def _original_path(self, asset_id: str) -> Path:
        return self._base / "originals" / asset_id

    def _thumb_path(self, asset_id: str) -> Path:
        return self._base / "thumbs" / f"{asset_id}.webp"

    def _public_path(self, asset_id: str) -> Path:
        return self._base / "public" / f"{asset_id}.webp"
