from dataclasses import dataclass

from score_state import ScoreState


@dataclass
class PrecheckResult:
    duplicate_found: bool
    explanation_category: str
    suggested_state: ScoreState
    context: str | None = None


_ZOO_CAPS: frozenset[str] = frozenset({"zoo_cap", "pet_cap"})


def run_precheck(
    animal_context: str,
    existing_sha256s: set[str],
    current_sha256: str | None,
) -> PrecheckResult:
    animal_context_lower = animal_context.lower() if animal_context else "unknown"

    is_duplicate = current_sha256 in existing_sha256s if current_sha256 else False

    if is_duplicate:
        return PrecheckResult(
            duplicate_found=True,
            explanation_category="duplicate_cap",
            suggested_state=ScoreState.CAPPED,
            context="duplicate",
        )

    if animal_context_lower == "zoo":
        return PrecheckResult(
            duplicate_found=False,
            explanation_category="zoo_cap",
            suggested_state=ScoreState.CAPPED,
            context="zoo",
        )

    if animal_context_lower == "pet":
        return PrecheckResult(
            duplicate_found=False,
            explanation_category="pet_cap",
            suggested_state=ScoreState.CAPPED,
            context="pet",
        )

    return PrecheckResult(
        duplicate_found=False,
        explanation_category="normal",
        suggested_state=ScoreState.AI_EVALUATED,
        context="wild" if animal_context_lower == "wild" else "unknown",
    )
