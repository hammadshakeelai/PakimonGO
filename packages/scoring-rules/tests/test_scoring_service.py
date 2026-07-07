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
    assert result.formula_version == "ai-v2"


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


class _RubricProvider:
    """Vision provider stub emitting the detailed ai-v2 rubric."""

    def __init__(self, detail, species="Aquila chrysaetos", context="wild"):
        self._detail = detail
        self._species = species
        self._context = context

    def analyze(self, media_path):
        return AnalysisResult(
            detected_species=self._species,
            confidence=0.9,
            suggested_context=self._context,
            raw_evidence={"provider": "test", "analysis": self._detail},
        )


def _rubric(rarity="common", respectful=False, disturbance=False,
            welfare=False, fake=False, sharp=0.0, comp=0.0, light=0.0,
            present=True):
    return {
        "animal_present": present,
        "rarity": rarity,
        "safety": {
            "respectful_distance": respectful,
            "signs_of_disturbance": disturbance,
            "welfare_concern": welfare,
        },
        "aesthetic": {"sharpness": sharp, "composition": comp, "lighting": light},
        "authenticity": {"suspected_fake": fake},
    }


def test_ai_v2_base_wild_is_25():
    svc = AIScoringService(vision_provider=_RubricProvider(_rubric()))
    r = svc.evaluate("wild", "normal", media_path="x.jpg")
    assert r.points == 25 and r.ledger == "wild"


def test_ai_v2_rarity_bonuses():
    for rarity, expected in [("uncommon", 35), ("rare", 50), ("exceptional", 65)]:
        svc = AIScoringService(
            vision_provider=_RubricProvider(_rubric(rarity=rarity)))
        assert svc.evaluate("wild", "normal", media_path="x.jpg").points == expected


def test_ai_v2_safety_bonus():
    svc = AIScoringService(
        vision_provider=_RubricProvider(_rubric(respectful=True)))
    assert svc.evaluate("wild", "normal", media_path="x.jpg").points == 35


def test_ai_v2_safety_bonus_denied_when_disturbed():
    svc = AIScoringService(
        vision_provider=_RubricProvider(
            _rubric(respectful=True, disturbance=True)))
    assert svc.evaluate("wild", "normal", media_path="x.jpg").points == 25


def test_ai_v2_aesthetic_bonus_tiers():
    svc = AIScoringService(vision_provider=_RubricProvider(
        _rubric(sharp=0.8, comp=0.8, light=0.8)))
    assert svc.evaluate("wild", "normal", media_path="x.jpg").points == 35
    svc = AIScoringService(vision_provider=_RubricProvider(
        _rubric(sharp=0.5, comp=0.6, light=0.5)))
    assert svc.evaluate("wild", "normal", media_path="x.jpg").points == 30


def test_ai_v2_max_stack_is_85():
    svc = AIScoringService(vision_provider=_RubricProvider(
        _rubric(rarity="exceptional", respectful=True,
                sharp=1.0, comp=1.0, light=1.0)))
    # 25 base + 40 exceptional + 10 safety + 10 aesthetic = 85 (< 90 cap)
    assert svc.evaluate("wild", "normal", media_path="x.jpg").points == 85


def test_ai_v2_welfare_concern_gates_to_review():
    svc = AIScoringService(
        vision_provider=_RubricProvider(_rubric(welfare=True)))
    r = svc.evaluate("wild", "normal", media_path="x.jpg")
    assert r.points == 1 and r.explanation_category == "welfare_review"


def test_ai_v2_suspected_fake_gates_to_zero():
    svc = AIScoringService(
        vision_provider=_RubricProvider(_rubric(fake=True)))
    r = svc.evaluate("wild", "normal", media_path="x.jpg")
    assert r.points == 0 and r.explanation_category == "authenticity_review"


def test_ai_v2_no_animal_gates_to_zero():
    svc = AIScoringService(vision_provider=_RubricProvider(
        _rubric(present=False), species=None))
    r = svc.evaluate("wild", "normal", media_path="x.jpg")
    assert r.points == 0 and r.explanation_category == "no_animal_detected"
