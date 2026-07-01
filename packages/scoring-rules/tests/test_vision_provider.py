import sys
from pathlib import Path
from unittest.mock import patch

_src = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(_src))

import pytest  # noqa: E402
from vision_provider import AnalysisResult, DummyVisionProvider  # noqa: E402


def test_dummy_provider_returns_analysis():
    provider = DummyVisionProvider()
    result = provider.analyze("/fake/path.jpg")
    assert isinstance(result, AnalysisResult)
    assert result.detected_species == "Passer domesticus"
    assert result.confidence == 0.95
    assert result.suggested_context == "wild"


def test_analysis_result_dataclass():
    r = AnalysisResult(
        detected_species="Canis lupus",
        confidence=0.88,
        suggested_context="wild",
        raw_evidence={"provider": "test"},
    )
    assert r.detected_species == "Canis lupus"
    assert r.confidence == 0.88
    assert r.raw_evidence == {"provider": "test"}


def test_analysis_result_defaults():
    r = AnalysisResult(
        detected_species=None,
        confidence=0.0,
        suggested_context="unknown",
    )
    assert r.raw_evidence is None


def test_google_provider_requires_key(monkeypatch):
    from google_vision_provider import GoogleVisionProvider
    monkeypatch.delenv("GOOGLE_VISION_API_KEY", raising=False)
    with pytest.raises(ValueError, match="requires GOOGLE_VISION_API_KEY"):
        GoogleVisionProvider()


MOCK_ZOO_RESPONSE = {
    "responses": [{
        "labelAnnotations": [
            {"description": "Zoo", "score": 0.98, "mid": "/m/0c6q0"},
            {"description": "Bird", "score": 0.95, "mid": "/m/015p6"},
            {"description": "Parrot", "score": 0.93, "mid": "/m/0gv1x"},
        ],
        "localizedObjectAnnotations": [
            {"name": "Parrot", "score": 0.92, "mid": "/m/0gv1x",
             "boundingPoly": {"normalizedVertices": [
                 {"x": 0.1, "y": 0.2}, {"x": 0.8, "y": 0.2},
                 {"x": 0.8, "y": 0.9}, {"x": 0.1, "y": 0.9}]}},
        ],
    }]
}

MOCK_WILD_RESPONSE = {
    "responses": [{
        "labelAnnotations": [
            {"description": "Wildlife", "score": 0.97, "mid": "/m/01yrx"},
            {"description": "Nature", "score": 0.95, "mid": "/m/05llg"},
            {"description": "Eagle", "score": 0.92, "mid": "/m/09kwv"},
        ],
        "localizedObjectAnnotations": [
            {"name": "Bird", "score": 0.89, "mid": "/m/015p6",
             "boundingPoly": {"normalizedVertices": [
                 {"x": 0.2, "y": 0.1}, {"x": 0.7, "y": 0.1},
                 {"x": 0.7, "y": 0.8}, {"x": 0.2, "y": 0.8}]}},
        ],
    }]
}

MOCK_PET_RESPONSE = {
    "responses": [{
        "labelAnnotations": [
            {"description": "Pet", "score": 0.96, "mid": "/m/068hy"},
            {"description": "Dog", "score": 0.98, "mid": "/m/0bt9lr"},
            {"description": "Mammal", "score": 0.94, "mid": "/m/0c6q0"},
        ],
        "localizedObjectAnnotations": [
            {"name": "Dog", "score": 0.97, "mid": "/m/0bt9lr",
             "boundingPoly": {"normalizedVertices": [
                 {"x": 0.1, "y": 0.1}, {"x": 0.9, "y": 0.1},
                 {"x": 0.9, "y": 0.9}, {"x": 0.1, "y": 0.9}]}},
        ],
    }]
}

MOCK_EMPTY_RESPONSE = {"responses": [{}]}

MOCK_ERROR_RESPONSE = {"error": {"code": 400, "message": "Bad request"}}


@pytest.fixture
def temp_image(tmp_path):
    img = tmp_path / "test.jpg"
    img.write_bytes(b"\xff\xd8\xff\xe0" + b"\x00" * 100)
    return str(img)


class TestGoogleVisionProvider:
    @patch("google_vision_provider.requests.post")
    def test_analyze_zoo(self, mock_post, temp_image):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = MOCK_ZOO_RESPONSE

        from google_vision_provider import GoogleVisionProvider
        provider = GoogleVisionProvider(api_key="test-key")
        result = provider.analyze(temp_image)

        assert result.detected_species == "Parrot"
        assert result.confidence == 0.98
        assert result.suggested_context == "zoo"
        assert result.raw_evidence == MOCK_ZOO_RESPONSE

    @patch("google_vision_provider.requests.post")
    def test_analyze_wild(self, mock_post, temp_image):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = MOCK_WILD_RESPONSE

        from google_vision_provider import GoogleVisionProvider
        provider = GoogleVisionProvider(api_key="test-key")
        result = provider.analyze(temp_image)

        assert result.detected_species == "Bird"
        assert result.confidence == 0.97
        assert result.suggested_context == "wild"

    @patch("google_vision_provider.requests.post")
    def test_analyze_pet(self, mock_post, temp_image):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = MOCK_PET_RESPONSE

        from google_vision_provider import GoogleVisionProvider
        provider = GoogleVisionProvider(api_key="test-key")
        result = provider.analyze(temp_image)

        assert result.detected_species == "Dog"
        assert result.confidence == 0.98
        assert result.suggested_context == "pet"

    @patch("google_vision_provider.requests.post")
    def test_analyze_empty_response(self, mock_post, temp_image):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = MOCK_EMPTY_RESPONSE

        from google_vision_provider import GoogleVisionProvider
        provider = GoogleVisionProvider(api_key="test-key")
        result = provider.analyze(temp_image)

        assert result.detected_species is None
        assert result.confidence == 0.0
        assert result.suggested_context == "unknown"

    @patch("google_vision_provider.requests.post")
    def test_analyze_error_response(self, mock_post, temp_image):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = MOCK_ERROR_RESPONSE

        from google_vision_provider import GoogleVisionProvider
        provider = GoogleVisionProvider(api_key="test-key")
        result = provider.analyze(temp_image)

        assert result.detected_species is None
        assert result.confidence == 0.0
        assert result.suggested_context == "unknown"

    @patch("google_vision_provider.requests.post")
    def test_analyze_http_error(self, mock_post, temp_image):
        import requests as req_lib
        mock_post.return_value.status_code = 403
        mock_post.return_value.raise_for_status.side_effect = (
            req_lib.exceptions.HTTPError("403 Forbidden")
        )

        from google_vision_provider import GoogleVisionProvider
        provider = GoogleVisionProvider(api_key="test-key")
        with pytest.raises(req_lib.exceptions.HTTPError):
            provider.analyze(temp_image)

    def test_analyze_file_not_found(self):
        from google_vision_provider import GoogleVisionProvider
        provider = GoogleVisionProvider(api_key="test-key")
        with pytest.raises(FileNotFoundError, match="not found"):
            provider.analyze("/nonexistent/path.jpg")
