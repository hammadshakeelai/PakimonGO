"""Cloud storage providers for production."""

import os
from pathlib import Path

_HAS_BOTO3 = False
_HAS_GCS = False
try:
    import boto3

    _HAS_BOTO3 = True
except ImportError:
    pass

try:
    from google.cloud import storage

    _HAS_GCS = True
except ImportError:
    pass


class StorageProvider:
    """Storage provider interface - duck typing compatible with LocalFileStorage."""

    def save_original(self, asset_id: str, content: bytes) -> str:
        """Save original file, return storage key."""
        ...

    def generate_derivative_stubs(self, asset_id: str) -> dict[str, str]:
        """Generate derivative stubs (thumbnail, public) and return URLs."""
        ...

    def get_url(self, key: str) -> str | None:
        """Get public URL for key."""
        ...

    def get_path(self, relative: str) -> Path | None:
        """Get local path for file (for local storage compatibility)."""
        ...


class S3StorageProvider(StorageProvider):
    """AWS S3 storage provider."""

    def __init__(self, bucket: str, region: str = "us-east-1"):
        if not _HAS_BOTO3:
            raise ImportError("boto3 required for S3StorageProvider")
        self._client = boto3.client("s3", region_name=region)
        self._bucket = bucket
        self._region = region

    def save_original(self, asset_id: str, content: bytes) -> str:
        key = f"originals/{asset_id}"
        self._client.put_object(Bucket=self._bucket, Key=key, Body=content)
        return key

    def generate_derivative_stubs(self, asset_id: str) -> dict[str, str]:
        return {
            "thumbnail": f"https://{self._bucket}.s3.{self._region}/thumbs/{asset_id}.webp",
            "public": f"https://{self._bucket}.s3.{self._region}/public/{asset_id}.webp",
        }

    def get_url(self, key: str) -> str | None:
        try:
            self._client.get_object(Bucket=self._bucket, Key=key)
            return f"https://{self._bucket}.s3.{self._region}.amazonaws.com/{key}"
        except Exception:
            return None

    def get_path(self, relative: str) -> Path | None:
        return None


class GCSStorageProvider(StorageProvider):
    """Google Cloud Storage provider."""

    def __init__(self, bucket_name: str):
        if not _HAS_GCS:
            raise ImportError("google-cloud-storage required for GCSStorageProvider")
        self._client = storage.Client()
        self._bucket_name = bucket_name
        self._bucket = self._client.bucket(bucket_name)

    def save_original(self, asset_id: str, content: bytes) -> str:
        key = f"originals/{asset_id}"
        blob = self._bucket.blob(key)
        blob.upload_from_string(content)
        return key

    def generate_derivative_stubs(self, asset_id: str) -> dict[str, str]:
        return {
            "thumbnail": f"https://storage.googleapis.com/{self._bucket_name}/thumbs/{asset_id}.webp",
            "public": f"https://storage.googleapis.com/{self._bucket_name}/public/{asset_id}.webp",
        }

    def get_url(self, key: str) -> str | None:
        blob = self._bucket.blob(key)
        if blob.exists():
            return blob.public_url
        return None

    def get_path(self, relative: str) -> Path | None:
        return None


def get_storage_provider() -> StorageProvider:
    """Factory for storage provider based on env vars."""
    provider = os.getenv("STORAGE_PROVIDER", "local")
    if provider == "s3":
        return S3StorageProvider(
            bucket=os.getenv("S3_BUCKET_NAME", "pakimongo-dev"),
            region=os.getenv("S3_REGION", "us-east-1"),
        )
    if provider == "gcs":
        return GCSStorageProvider(bucket_name=os.getenv("GCS_BUCKET_NAME", "pakimongo-dev"))
    from .local_storage import LocalFileStorage

    return LocalFileStorage()
