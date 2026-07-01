import sys
from pathlib import Path

_src = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(_src))

from scoring_service import AIScoringService, ScoringResult, StubScoringService  # noqa: E402
from vision_provider import AnalysisResult  # noqa: E402


def test_wild_scores_25():
    svc = StubScoringService()
    result = svc.evaluate("wild", "normal")
    assert result.points == 25
    assert result.ledger == "wild"
    assert result.formula_version == "stub-v1"


def test_zoo_scores_1():
    svc = StubScoringService()
    result = svc.evaluate("zoo", "zoo_cap")
    assert result.points == 1
    assert result.ledger == "participation"


def test_pet_scores_1():
    svc = StubScoringService()
    result = svc.evaluate("pet", "pet_cap")
    assert result.points == 1
    assert result.ledger == "pet_social"


def test_duplicate_scores_0():
    svc = StubScoringService()
    result = svc.evaluate("wild", "duplicate_cap")
    assert result.points == 0
    assert result.ledger == "participation"


def test_unknown_context_defaults_to_wild():
    svc = StubScoringService()
    result = svc.evaluate("unknown", "normal")
    assert result.points == 25
    assert result.ledger == "wild"


def test_scoring_result_dataclass():
    r = ScoringResult(points=10, ledger="wild", explanation_category="normal", formula_version="v1")
    assert r.points == 10
    assert r.ledger == "wild"


class _DummyProvider:
    def __init__(self, ctx: str = "wild"):
        self._ctx = ctx
    def analyze(self, media_path: str) -> AnalysisResult:
        return AnalysisResult(
            detected_species="Testus specimen",
            confidence=0.99,
            suggested_context=self._ctx,
        )


def test_ai_service_with_vision_provider_wild():
    provider = _DummyProvider("wild")
    svc = AIScoringService(vision_provider=provider)
    result = svc.evaluate("unknown", "normal", media_path="/fake/path.jpg")
    assert result.points == 25
    assert result.ledger == "wild"
    assert result.formula_version == "ai-v1"


def test_ai_service_with_vision_provider_zoo():
    provider = _DummyProvider("zoo")
    svc = AIScoringService(vision_provider=provider)
    result = svc.evaluate("unknown", "normal", media_path="/fake/path.jpg")
    assert result.points == 1
    assert result.ledger == "participation"
    assert result.explanation_category == "zoo_cap"


def test_ai_service_with_vision_provider_pet():
    provider = _DummyProvider("pet")
    svc = AIScoringService(vision_provider=provider)
    result = svc.evaluate("unknown", "normal", media_path="/fake/path.jpg")
    assert result.points == 1
    assert result.ledger == "pet_social"


def test_ai_service_capped_path_uses_fallback():
    provider = _DummyProvider("wild")
    svc = AIScoringService(vision_provider=provider)
    result = svc.evaluate("zoo", "zoo_cap")
    assert result.points == 1
    assert result.formula_version == "stub-v1"


def test_ai_service_no_provider_fallback():
    svc = AIScoringService()
    result = svc.evaluate("wild", "normal")
    assert result.points == 25
    assert result.formula_version == "stub-v1"


def test_ai_service_no_media_path_fallback():
    provider = _DummyProvider("wild")
    svc = AIScoringService(vision_provider=provider)
    result = svc.evaluate("wild", "normal")
    assert result.points == 25
    assert result.formula_version == "stub-v1"
