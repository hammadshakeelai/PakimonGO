import os

from vision_provider import AnalysisResult


class GoogleVisionProvider:
    ENV_KEY = "GOOGLE_VISION_API_KEY"

    def __init__(self, api_key: str | None = None):
        self._api_key = api_key or os.environ.get(self.ENV_KEY)
        if not self._api_key:
            raise ValueError(
                f"GoogleVisionProvider requires {self.ENV_KEY} env var or api_key argument"
            )

    def analyze(self, media_path: str) -> AnalysisResult:
        raise NotImplementedError("GoogleVisionProvider not yet implemented")
