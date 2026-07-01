import base64
import os
from pathlib import Path

import requests

from vision_provider import AnalysisResult


class GoogleVisionProvider:
    ENDPOINT = "https://vision.googleapis.com/v1/images:annotate"
    ENV_KEY = "GOOGLE_VISION_API_KEY"
    _ZOO_KEYWORDS = frozenset({"zoo", "aviary", "enclosure", "captivity", "exhibit", "menagerie"})
    _PET_KEYWORDS = frozenset({"pet", "domestic", "dog", "cat", "indoor", "kitten", "puppy"})
    _TIMEOUT = 30

    def __init__(self, api_key: str | None = None):
        self._api_key = api_key or os.environ.get(self.ENV_KEY)
        if not self._api_key:
            raise ValueError(
                f"GoogleVisionProvider requires {self.ENV_KEY} env var or api_key argument"
            )

    def analyze(self, media_path: str) -> AnalysisResult:
        image_path = Path(media_path)
        if not image_path.exists():
            raise FileNotFoundError(f"Image not found: {media_path}")

        encoded = base64.b64encode(image_path.read_bytes()).decode("utf-8")
        payload = {
            "requests": [{
                "image": {"content": encoded},
                "features": [
                    {"type": "LABEL_DETECTION", "maxResults": 10},
                    {"type": "OBJECT_LOCALIZATION", "maxResults": 5},
                ],
            }]
        }

        resp = requests.post(
            f"{self.ENDPOINT}?key={self._api_key}",
            json=payload,
            timeout=self._TIMEOUT,
        )
        resp.raise_for_status()
        return self._parse_response(resp.json())

    @classmethod
    def _parse_response(cls, data: dict) -> AnalysisResult:
        responses = data.get("responses", [])
        if not responses:
            return AnalysisResult(
                detected_species=None,
                confidence=0.0,
                suggested_context="unknown",
                raw_evidence=data,
            )

        annotations = responses[0].get("labelAnnotations", [])
        objects = responses[0].get("localizedObjectAnnotations", [])

        best_label: str | None = None
        best_score = 0.0
        labels_lower: list[str] = []
        for ann in annotations:
            desc = ann.get("description", "")
            score = ann.get("score", 0.0)
            labels_lower.append(desc.lower())
            if score > best_score:
                best_label = desc
                best_score = score

        species: str | None = None
        for obj in objects:
            name = obj.get("name", "")
            if name and obj.get("score", 0) > 0.5:
                species = name
                break
        if species is None:
            species = best_label

        return AnalysisResult(
            detected_species=species,
            confidence=best_score,
            suggested_context=cls._classify_context(labels_lower),
            raw_evidence=data,
        )

    @classmethod
    def _classify_context(cls, labels: list[str]) -> str:
        if not labels:
            return "unknown"
        for label in labels:
            for kw in cls._ZOO_KEYWORDS:
                if kw in label:
                    return "zoo"
            for kw in cls._PET_KEYWORDS:
                if kw in label:
                    return "pet"
        return "wild"
