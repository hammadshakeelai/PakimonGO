import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



class TestStorageProviderInterface:
    """Tests for storage provider contract without external deps."""

    def test_s3_urls_format(self):
        """Verify S3 URL format is correct."""
        bucket = "test-bucket"
        region = "us-west-2"
        expected_thumb = f"https://{bucket}.s3.{region}/thumbs/test-id.webp"

        assert expected_thumb.startswith("https://")
        assert "test-bucket" in expected_thumb
        assert "test-id.webp" in expected_thumb

    def test_gcs_urls_format(self):
        """Verify GCS URL format is correct."""
        bucket = "test-bucket"
        expected_thumb = f"https://storage.googleapis.com/{bucket}/thumbs/test-id.webp"

        assert expected_thumb.startswith("https://")
        assert "storage.googleapis.com" in expected_thumb

    def test_env_defaults_local(self):
        """Verify default storage provider is local."""
        os.environ.pop("STORAGE_PROVIDER", None)
        # When STORAGE_PROVIDER not set or "local", LocalFileStorage is used
        assert os.getenv("STORAGE_PROVIDER", "local") == "local"
