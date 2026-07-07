from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass
class ScoringResult:
    points: int
    ledger: str
    explanation_category: str
    formula_version: str


class ScoringService(Protocol):
    def evaluate(
        self,
        animal_context: str,
        explanation_category: str,
        media_path: str | None = None,
    ) -> ScoringResult:
        ...


class StubScoringService:
    FORMULA_VERSION = "stub-v1"

    def evaluate(
        self,
        animal_context: str,
        explanation_category: str,
        media_path: str | None = None,
    ) -> ScoringResult:
        ctx = animal_context.lower() if animal_context else "unknown"

        if explanation_category in ("duplicate_cap",):
            return ScoringResult(
                points=0,
                ledger="participation",
                explanation_category="duplicate_cap",
                formula_version=self.FORMULA_VERSION,
            )

        if ctx == "zoo":
            return ScoringResult(
                points=1,
                ledger="participation",
                explanation_category="zoo_cap",
                formula_version=self.FORMULA_VERSION,
            )

        if ctx == "pet":
            return ScoringResult(
                points=1,
                ledger="pet_social",
                explanation_category="pet_cap",
                formula_version=self.FORMULA_VERSION,
            )

        return ScoringResult(
            points=25,
            ledger="wild",
            explanation_category="normal",
            formula_version=self.FORMULA_VERSION,
        )


class AIScoringService:
    """Scores from the vision rubric (formula ai-v2).

    Wild base 25, plus:
    - rarity bonus:   uncommon +10 / rare +25 / exceptional +40
    - safety bonus:   +10 when the photographer kept respectful distance
                      and the animal shows no disturbance
    - aesthetic bonus: mean(sharpness, composition, lighting) >= 0.7 -> +10,
                      >= 0.5 -> +5
    Hard gates (checked first):
    - no animal detected            -> 0 pts, "no_animal_detected"
    - suspected fake / screen photo -> 0 pts, "authenticity_review"
    - welfare concern               -> 1 pt,  "welfare_review"
    Zoo and pet stay capped at 1. Total is capped at 90. Providers without
    the detailed rubric (e.g. the dummy provider) score the classic wild 25.
    """

    FORMULA_VERSION = "ai-v2"
    _RARITY_BONUS = {"uncommon": 10, "rare": 25, "exceptional": 40}
    _MAX_POINTS = 90

    def __init__(self, vision_provider=None):
        self._provider = vision_provider
        self._fallback = StubScoringService()

    def evaluate(
        self,
        animal_context: str,
        explanation_category: str,
        media_path: str | None = None,
    ) -> ScoringResult:
        if explanation_category in ("duplicate_cap", "zoo_cap", "pet_cap"):
            return self._fallback.evaluate(animal_context, explanation_category)

        if self._provider is not None and media_path:
            analysis = self._provider.analyze(media_path)
            return self._score_analysis(analysis)

        return self._fallback.evaluate(animal_context, explanation_category)

    def _score_analysis(self, analysis) -> ScoringResult:
        detail = {}
        raw = getattr(analysis, "raw_evidence", None)
        if isinstance(raw, dict):
            candidate = raw.get("analysis")
            if isinstance(candidate, dict):
                detail = candidate

        authenticity = detail.get("authenticity") or {}
        if authenticity.get("suspected_fake") is True:
            return ScoringResult(
                points=0,
                ledger="participation",
                explanation_category="authenticity_review",
                formula_version=self.FORMULA_VERSION,
            )

        if detail.get("animal_present") is False or (
            detail and analysis.detected_species is None
        ):
            return ScoringResult(
                points=0,
                ledger="participation",
                explanation_category="no_animal_detected",
                formula_version=self.FORMULA_VERSION,
            )

        ctx = analysis.suggested_context.lower()
        if ctx == "zoo":
            return ScoringResult(
                points=1,
                ledger="participation",
                explanation_category="zoo_cap",
                formula_version=self.FORMULA_VERSION,
            )
        if ctx == "pet":
            return ScoringResult(
                points=1,
                ledger="pet_social",
                explanation_category="pet_cap",
                formula_version=self.FORMULA_VERSION,
            )

        safety = detail.get("safety") or {}
        if safety.get("welfare_concern") is True:
            return ScoringResult(
                points=1,
                ledger="participation",
                explanation_category="welfare_review",
                formula_version=self.FORMULA_VERSION,
            )

        points = 25
        points += self._RARITY_BONUS.get(str(detail.get("rarity", "")).lower(), 0)
        if (
            safety.get("respectful_distance") is True
            and safety.get("signs_of_disturbance") is not True
        ):
            points += 10
        aesthetic = detail.get("aesthetic") or {}
        try:
            scores = [
                float(aesthetic.get(k, 0.0))
                for k in ("sharpness", "composition", "lighting")
            ]
            mean = sum(scores) / 3
        except (TypeError, ValueError):
            mean = 0.0
        if mean >= 0.7:
            points += 10
        elif mean >= 0.5:
            points += 5

        return ScoringResult(
            points=min(points, self._MAX_POINTS),
            ledger="wild",
            explanation_category="normal",
            formula_version=self.FORMULA_VERSION,
        )
