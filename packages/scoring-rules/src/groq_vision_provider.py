from __future__ import annotations

import base64
import json
import os
from pathlib import Path

import requests

from vision_provider import AnalysisResult


class GroqVisionProvider:
    """Free-tier vision provider backed by a Groq multimodal LLM.

    Uses the OpenAI-compatible chat-completions endpoint with an image data URI
    and asks the model for a strict JSON verdict (species + wild/zoo/pet context).
    Requires GROQ_API_KEY (no billing account needed). The model is overridable
    via GROQ_MODEL since Groq's vision line-up changes over time.
    """

    ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"
    ENV_KEY = "GROQ_API_KEY"
    DEFAULT_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"
    _VALID_CONTEXTS = frozenset({"wild", "zoo", "pet", "unknown"})
    _TIMEOUT = 30
    _PROMPT = (
        "You are a wildlife identification assistant. Identify the single most "
        "prominent animal in the photo and whether it was taken in the wild, in a "
        "zoo/aquarium/captivity, or is a domestic pet. Respond with ONLY a JSON "
        'object and no other text: {"species": string or null, "context": one of '
        '"wild"|"zoo"|"pet"|"unknown", "confidence": number between 0 and 1}.'
    )

    def __init__(self, api_key: str | None = None, model: str | None = None) -> None:
        self._api_key = api_key or os.environ.get(self.ENV_KEY)
        if not self._api_key:
            raise ValueError(
                f"GroqVisionProvider requires {self.ENV_KEY} env var or api_key argument"
            )
        self._model = model or os.environ.get("GROQ_MODEL", self.DEFAULT_MODEL)

    def analyze(self, media_path: str) -> AnalysisResult:
        image_path = Path(media_path)
        if not image_path.exists():
            raise FileNotFoundError(f"Image not found: {media_path}")

        mime = "image/png" if image_path.suffix.lower() == ".png" else "image/jpeg"
        encoded = base64.b64encode(image_path.read_bytes()).decode("utf-8")
        payload = {
            "model": self._model,
            "messages": [{
                "role": "user",
                "content": [
                    {"type": "text", "text": self._PROMPT},
                    {"type": "image_url",
                     "image_url": {"url": f"data:{mime};base64,{encoded}"}},
                ],
            }],
            "temperature": 0,
            "max_tokens": 200,
            "response_format": {"type": "json_object"},
        }
        resp = requests.post(
            self.ENDPOINT,
            headers={
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=self._TIMEOUT,
        )
        resp.raise_for_status()
        return self._parse_response(resp.json())

    @classmethod
    def _parse_response(cls, data: dict) -> AnalysisResult:
        try:
            content = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError):
            return AnalysisResult(None, 0.0, "unknown",
                                  {"provider": "groq", "error": "no_content", "raw": data})

        parsed = cls._extract_json(content)
        species = parsed.get("species") or None
        context = str(parsed.get("context", "unknown")).lower()
        if context not in cls._VALID_CONTEXTS:
            context = "unknown"
        try:
            confidence = max(0.0, min(1.0, float(parsed.get("confidence", 0.0))))
        except (TypeError, ValueError):
            confidence = 0.0
        return AnalysisResult(
            detected_species=species,
            confidence=confidence,
            suggested_context=context,
            raw_evidence={"provider": "groq", "content": content},
        )

    @staticmethod
    def _extract_json(content: str) -> dict:
        text = content.strip()
        if text.startswith("```"):
            text = text.strip("`")
            newline = text.find("\n")
            if newline != -1:
                text = text[newline + 1:]
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            start, end = text.find("{"), text.rfind("}")
            if 0 <= start < end:
                try:
                    return json.loads(text[start:end + 1])
                except json.JSONDecodeError:
                    return {}
            return {}
