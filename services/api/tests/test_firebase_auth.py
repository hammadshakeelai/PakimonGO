"""Unit tests for FirebaseAuthAdapter using an injected verifier.

These exercise the claim-mapping and error handling without the firebase-admin
dependency or live credentials. The env-based selection defaults to the fake
adapter, so the rest of the suite is unaffected.
"""

import pytest

from src.infrastructure.auth.firebase_adapter import FirebaseAuthAdapter


def test_maps_claims_to_user_context():
    adapter = FirebaseAuthAdapter(
        verifier=lambda _t: {"uid": "u123", "email": "a@b.com"}
    )
    ctx = adapter.verify_token("good-token")
    assert ctx.user_id == "u123"
    assert ctx.email == "a@b.com"
    assert ctx.auth_provider == "firebase"


def test_falls_back_to_sub_claim():
    adapter = FirebaseAuthAdapter(verifier=lambda _t: {"sub": "u456"})
    assert adapter.verify_token("t").user_id == "u456"


def test_invalid_token_raises_permission_error():
    def boom(_t):
        raise RuntimeError("bad token")

    adapter = FirebaseAuthAdapter(verifier=boom)
    with pytest.raises(PermissionError):
        adapter.verify_token("bad-token")


def test_missing_uid_raises_permission_error():
    adapter = FirebaseAuthAdapter(verifier=lambda _t: {"email": "a@b.com"})
    with pytest.raises(PermissionError):
        adapter.verify_token("no-uid")
