import sys
from pathlib import Path

_src = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(_src))

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
    import pytest
    monkeypatch.delenv("GOOGLE_VISION_API_KEY", raising=False)
    with pytest.raises(ValueError, match="requires GOOGLE_VISION_API_KEY"):
        GoogleVisionProvider()


def test_google_provider_not_implemented():
    from google_vision_provider import GoogleVisionProvider
    import pytest
    provider = GoogleVisionProvider(api_key="test-key-123")
    with pytest.raises(NotImplementedError):
        provider.analyze("/fake/path.jpg")
