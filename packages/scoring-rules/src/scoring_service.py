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
    FORMULA_VERSION = "ai-v1"

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
            return ScoringResult(
                points=25,
                ledger="wild",
                explanation_category="normal",
                formula_version=self.FORMULA_VERSION,
            )

        return self._fallback.evaluate(animal_context, explanation_category)
