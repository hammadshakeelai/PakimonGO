import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest

from src.infrastructure.storage.cloud_storage import (
    S3StorageProvider,
    GCSStorageProvider,
    get_storage_provider,
)


class TestStorageProviderFactory:

    def test_default_is_local(self):
        os.environ.pop("STORAGE_PROVIDER", None)
        from src.infrastructure.storage.local_storage import LocalFileStorage
        provider = get_storage_provider()
        assert isinstance(provider, LocalFileStorage)

    def test_s3_provider_requires_boto3(self):
        os.environ["STORAGE_PROVIDER"] = "s3"
        with pytest.raises(ImportError, match="boto3"):
            get_storage_provider()

    def test_gcs_provider_requires_gcs(self):
        os.environ["STORAGE_PROVIDER"] = "gcs"
        # Without the google-cloud-storage lib this raises ImportError; when the lib
        # is present (e.g. pulled in by firebase-admin) it fails on missing GCS
        # credentials instead. Either way, gcs is not usable without real setup.
        with pytest.raises(Exception):
            get_storage_provider()
        os.environ.pop("STORAGE_PROVIDER", None)


class TestS3StorageProvider:

    def test_derivative_stubs_urls(self):
        provider = S3StorageProvider.__new__(S3StorageProvider)
        provider._bucket = "test-bucket"
        provider._region = "us-west-2"
        urls = provider.generate_derivative_stubs("asset-123")
        assert urls["thumbnail"] == "https://test-bucket.s3.us-west-2/thumbs/asset-123.webp"
        assert urls["public"] == "https://test-bucket.s3.us-west-2/public/asset-123.webp"

    def test_get_path_returns_none(self):
        provider = S3StorageProvider.__new__(S3StorageProvider)
        assert provider.get_path("some/path") is None


class TestGCSStorageProvider:

    def test_derivative_stubs_urls(self):
        provider = GCSStorageProvider.__new__(GCSStorageProvider)
        provider._bucket_name = "test-bucket"
        urls = provider.generate_derivative_stubs("asset-123")
        assert urls["thumbnail"] == "https://storage.googleapis.com/test-bucket/thumbs/asset-123.webp"
        assert urls["public"] == "https://storage.googleapis.com/test-bucket/public/asset-123.webp"

    def test_get_path_returns_none(self):
        provider = GCSStorageProvider.__new__(GCSStorageProvider)
        assert provider.get_path("some/path") is None


class TestMediaRoutesWithCloudStorage:

    def test_media_upload_local_provider(self):
        os.environ["STORAGE_PROVIDER"] = "local"
        from fastapi.testclient import TestClient
        from src.main import app
        client = TestClient(app)
        auth = {"Authorization": "Bearer test_token_valid"}

        resp = client.post("/v1/media/upload-intent", json={
            "fileName": "test.jpg",
            "contentType": "image/jpeg",
            "byteSize": 500000,
            "sha256": "c" * 64,
        }, headers=auth)
        assert resp.status_code == 200
        media_id = resp.json()["mediaAssetId"]

        upload = client.put(
            f"/v1/media/upload/{media_id}",
            files={"file": ("test.jpg", b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01" + b"\x00" * 64, "image/jpeg")},
            headers=auth,
        )
        assert upload.status_code == 200

        complete = client.post("/v1/media/complete-upload", json={
            "mediaAssetId": media_id,
            "sha256": "c" * 64,
        }, headers=auth)
        assert complete.status_code == 200
        derivs = complete.json()["derivatives"]
        assert derivs["thumbnailUrl"] is not None
        assert derivs["derivativeUrl"] is not None
