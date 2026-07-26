from __future__ import annotations

from pathlib import Path


class StorageProvider:
    """Storage provider interface."""

    def save_original(self, asset_id: str, content: bytes) -> str:
        """Save original file, return storage key."""
        raise NotImplementedError

    def generate_derivative_stubs(self, asset_id: str) -> dict[str, object]:
        """Generate derivative stubs (thumbnail, public) and return URLs plus
        an `exif_stripped: bool` reflecting whether metadata was actually
        removed - callers must not assume True without checking it."""
        raise NotImplementedError

    def get_url(self, key: str) -> str | None:
        """Get public URL for key."""
        raise NotImplementedError

    def get_path(self, relative: str) -> Path | None:
        """Get local path for file (for local storage compatibility)."""
        raise NotImplementedError
