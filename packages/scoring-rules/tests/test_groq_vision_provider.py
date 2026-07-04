import sys
from pathlib import Path
from unittest.mock import patch

_src = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(_src))

import pytest  # noqa: E402


def _groq_response(content: str) -> dict:
    return {"choices": [{"message": {"content": content}}]}


@pytest.fixture
def temp_image(tmp_path):
    img = tmp_path / "test.jpg"
    img.write_bytes(b"\xff\xd8\xff\xe0" + b"\x00" * 100)
    return str(img)


def test_requires_key(monkeypatch):
    from groq_vision_provider import GroqVisionProvider
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    with pytest.raises(ValueError, match="requires GROQ_API_KEY"):
        GroqVisionProvider()


class TestGroqVisionProvider:
    @patch("groq_vision_provider.requests.post")
    def test_analyze_wild(self, mock_post, temp_image):
        mock_post.return_value.json.return_value = _groq_response(
            '{"species": "Bald Eagle", "context": "wild", "confidence": 0.91}'
        )
        from groq_vision_provider import GroqVisionProvider
        result = GroqVisionProvider(api_key="test-key").analyze(temp_image)
        assert result.detected_species == "Bald Eagle"
        assert result.suggested_context == "wild"
        assert result.confidence == 0.91

    @patch("groq_vision_provider.requests.post")
    def test_analyze_zoo_with_markdown_fence(self, mock_post, temp_image):
        mock_post.return_value.json.return_value = _groq_response(
            '```json\n{"species": "Peacock", "context": "ZOO", "confidence": 0.8}\n```'
        )
        from groq_vision_provider import GroqVisionProvider
        result = GroqVisionProvider(api_key="test-key").analyze(temp_image)
        assert result.detected_species == "Peacock"
        assert result.suggested_context == "zoo"  # normalized to lowercase

    @patch("groq_vision_provider.requests.post")
    def test_invalid_context_becomes_unknown(self, mock_post, temp_image):
        mock_post.return_value.json.return_value = _groq_response(
            '{"species": "Thing", "context": "spaceship", "confidence": 2.0}'
        )
        from groq_vision_provider import GroqVisionProvider
        result = GroqVisionProvider(api_key="test-key").analyze(temp_image)
        assert result.suggested_context == "unknown"
        assert result.confidence == 1.0  # clamped to [0, 1]

    @patch("groq_vision_provider.requests.post")
    def test_prose_wrapped_json_is_extracted(self, mock_post, temp_image):
        mock_post.return_value.json.return_value = _groq_response(
            'Here is the result: {"species": "Dog", "context": "pet", "confidence": 0.7} thanks'
        )
        from groq_vision_provider import GroqVisionProvider
        result = GroqVisionProvider(api_key="test-key").analyze(temp_image)
        assert result.suggested_context == "pet"
        assert result.detected_species == "Dog"

    @patch("groq_vision_provider.requests.post")
    def test_unparseable_content_is_safe(self, mock_post, temp_image):
        mock_post.return_value.json.return_value = _groq_response("sorry, I cannot tell")
        from groq_vision_provider import GroqVisionProvider
        result = GroqVisionProvider(api_key="test-key").analyze(temp_image)
        assert result.detected_species is None
        assert result.suggested_context == "unknown"
        assert result.confidence == 0.0

    @patch("groq_vision_provider.requests.post")
    def test_http_error_propagates(self, mock_post, temp_image):
        import requests as req_lib
        mock_post.return_value.raise_for_status.side_effect = (
            req_lib.exceptions.HTTPError("401 Unauthorized")
        )
        from groq_vision_provider import GroqVisionProvider
        with pytest.raises(req_lib.exceptions.HTTPError):
            GroqVisionProvider(api_key="test-key").analyze(temp_image)

    def test_file_not_found(self):
        from groq_vision_provider import GroqVisionProvider
        provider = GroqVisionProvider(api_key="test-key")
        with pytest.raises(FileNotFoundError, match="not found"):
            provider.analyze("/nonexistent/path.jpg")
