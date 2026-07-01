from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass
class AnalysisResult:
    detected_species: str | None
    confidence: float
    suggested_context: str
    raw_evidence: dict | None = None


class VisionProvider(Protocol):
    def analyze(self, media_path: str) -> AnalysisResult:
        ...


class DummyVisionProvider:
    def analyze(self, media_path: str) -> AnalysisResult:
        return AnalysisResult(
            detected_species="Passer domesticus",
            confidence=0.95,
            suggested_context="wild",
            raw_evidence={"provider": "dummy", "model": "dummy-v1"},
        )
