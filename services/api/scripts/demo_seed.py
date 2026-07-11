"""Demo content seed — proof-of-concept data owned by a root demo user.

Activated with ``DEMO_SEED=1`` (checked at API startup). Idempotent for
database rows; image files are re-materialized on every boot because hosts
like Render keep uploads on ephemeral disk.

Creates the official demo account with real stored photos (originals +
webp derivatives via the normal storage pipeline), scored submissions
spread around Islamabad, and a few notifications — so a fresh install of
the app shows a living map, history, collection, and leaderboard.
"""

from __future__ import annotations

import hashlib
import logging
from pathlib import Path

from sqlalchemy.orm import Session

log = logging.getLogger("demo_seed")

DEMO_USER_ID = "pakimongo_official"

# Additional community accounts so the feed and leaderboard feel alive.
# (file, owner) — files come from the same demo asset pool.
COMMUNITY = [
    ("card_kingfisher.jpg", "wildlens_aisha", "Alcedo atthis", "wild", 60, 33.7511, 73.1022,
     "Patience pays off at the lake edge."),
    ("hero_sparrow.jpg", "trailcam_omar", "Passer domesticus", "wild", 25, 33.7233, 73.0644,
     "Morning regular at the feeder tree."),
    ("card_myna.jpg", "safeshot_sara", "Acridotheres tristis", "wild", 20, 33.6977, 73.0512,
     "Mynas own this park and they know it."),
    ("thumb_butterfly.jpg", "wildlens_aisha", "Danaus chrysippus", "wild", 30, 33.7150, 73.0898,
     "Wings out in the noon sun."),
]
_ASSETS = Path(__file__).resolve().parents[1] / "assets" / "demo"

# (file, scientific name, cute name, context, points, lat, lng, caption)
DEMO_CAPTURES = [
    ("card_kingfisher.jpg", "Alcedo atthis", "Sapphire", "wild", 65, 33.7294, 73.0931,
     "Common Kingfisher scanning Rawal Lake at golden hour."),
    ("card_eagle.jpg", "Aquila chrysaetos", "Ranger", "wild", 75, 33.7782, 73.0812,
     "Golden Eagle riding thermals over the Margalla ridgeline."),
    ("hero_sparrow.jpg", "Passer domesticus", "Chirpy", "wild", 25, 33.7100, 73.0551,
     "House Sparrow in the morning light — life thrives everywhere."),
    ("hero_bulbul.jpg", "Pycnonotus cafer", "Rafi", "wild", 45, 33.6938, 73.0652,
     "Red-vented Bulbul singing after the rain."),
    ("card_myna.jpg", "Acridotheres tristis", "Scout", "wild", 20, 33.6844, 73.0479,
     "Common Myna patrolling the park path."),
    ("thumb_butterfly.jpg", "Danaus chrysippus", "Amber", "wild", 30, 33.7008, 73.0790,
     "Plain Tiger butterfly on garden lantana."),
    ("card_peafowl.jpg", "Pavo cristatus", "Raja", "zoo", 1, 33.7069, 73.1113,
     "Indian Peafowl at the wildlife park — capped, honesty first."),
    ("card_retriever.jpg", "Canis familiaris", "Buddy", "pet", 1, 33.6900, 73.0300,
     "Golden Retriever — pet shots are capped but still collectible."),
]


def run_demo_seed(db: Session) -> bool:
    """Seed demo content. Returns True when rows were created this run."""
    from src.infrastructure.database.models import (
        CaptureLocation,
        PublicLocationCell,
        Submission,
        SubmissionAttribute,
        User,
    )
    from src.infrastructure.database.repositories import (
        complete_media_asset,
        create_media_asset,
        create_notification,
        create_score_event,
        update_submission_status,
    )
    from src.infrastructure.storage.local_storage import LocalFileStorage

    if not _ASSETS.exists():
        log.warning("demo assets folder missing: %s", _ASSETS)
        return False

    storage = LocalFileStorage()

    user = db.query(User).filter(User.id == DEMO_USER_ID).first()
    already_seeded = user is not None
    if user is None:
        user = User(id=DEMO_USER_ID, trust_state="verified",
                    age_band="adult", home_region="PK")
        db.add(user)
        db.commit()

    if already_seeded:
        # Rows exist — re-materialize files on ephemeral disks, and seed
        # any community accounts added since the first deploy.
        _restore_files(db, storage)
        _seed_community(db, storage)
        _seed_social(db, storage)
        return False

    for file_name, species, cute, context, points, lat, lng, caption in DEMO_CAPTURES:
        content = (_ASSETS / file_name).read_bytes()
        sha = hashlib.sha256(content).hexdigest()

        asset = create_media_asset(
            db, file_name, "image/jpeg", len(content), sha,
            owner_user_id=DEMO_USER_ID,
        )
        storage.save_original(asset.id, content)
        storage.generate_derivative_stubs(asset.id)
        complete_media_asset(db, asset.id, sha)

        sub = Submission(user_id=DEMO_USER_ID, primary_media_asset_id=asset.id,
                         status="scored", visibility="private")
        db.add(sub)
        db.flush()
        db.add(SubmissionAttribute(
            submission_id=sub.id, animal_context=context, real_name=species,
            cute_name=cute, caption=caption, tags=context,
        ))
        db.add(CaptureLocation(
            submission_id=sub.id, latitude=lat, longitude=lng,
            accuracy_meters=12.0, source="gps",
        ))
        cell_lat, cell_lng = round(lat, 2), round(lng, 2)
        db.add(PublicLocationCell(
            submission_id=sub.id,
            cell_id=f"cell_{cell_lat:.2f}_{cell_lng:.2f}",
            precision_label="cell",
        ))
        db.commit()
        update_submission_status(db, sub.id, "scored")
        ledger = "wild" if context == "wild" else (
            "pet_social" if context == "pet" else "participation")
        create_score_event(
            db=db, submission_id=sub.id, user_id=DEMO_USER_ID, ledger=ledger,
            points=points, event_type="scored", formula_version="ai-v2",
            explanation_category="normal" if context == "wild" else f"{context}_cap",
            previous_state="ai_evaluated", new_state="scored",
        )
        create_notification(
            db, DEMO_USER_ID, "submission_scored",
            f"{species.split()[0]} scored!",
            body=f"Your {cute} earned {points} points",
            reference_type="submission", reference_id=sub.id,
        )

    _seed_community(db, storage)
    _seed_social(db, storage)

    log.info("demo seed created %d captures for %s", len(DEMO_CAPTURES), DEMO_USER_ID)
    return True


def _seed_social(db: Session, storage) -> None:
    """Wave 2: real CC wildlife photos, comments, reactions, live stories."""
    from demo_seed_social import seed_social_wave

    seed_social_wave(db, storage)


def _seed_community(db: Session, storage) -> None:
    """Idempotent per-account seeding for the community demo users."""
    from src.infrastructure.database.models import (
        CaptureLocation,
        Submission,
        SubmissionAttribute,
        User,
    )
    from src.infrastructure.database.repositories import (
        complete_media_asset,
        create_media_asset,
        create_score_event,
        update_submission_status,
    )

    for file_name, owner, species, context, points, lat, lng, caption in COMMUNITY:
        if db.query(User).filter(User.id == owner).first() is not None:
            continue  # this account already seeded
        db.add(User(id=owner, trust_state="verified", age_band="adult", home_region="PK"))
        db.commit()
        content = (_ASSETS / file_name).read_bytes()
        sha = hashlib.sha256(content + owner.encode()).hexdigest()
        asset = create_media_asset(
            db, file_name, "image/jpeg", len(content), sha, owner_user_id=owner)
        storage.save_original(asset.id, content)
        storage.generate_derivative_stubs(asset.id)
        complete_media_asset(db, asset.id, sha)
        sub = Submission(user_id=owner, primary_media_asset_id=asset.id,
                         status="scored", visibility="private")
        db.add(sub)
        db.flush()
        db.add(SubmissionAttribute(
            submission_id=sub.id, animal_context=context, real_name=species,
            cute_name=species.split()[0], caption=caption, tags=context))
        db.add(CaptureLocation(submission_id=sub.id, latitude=lat, longitude=lng,
                               accuracy_meters=15.0, source="gps"))
        db.commit()
        update_submission_status(db, sub.id, "scored")
        create_score_event(
            db=db, submission_id=sub.id, user_id=owner, ledger="wild",
            points=points, event_type="scored", formula_version="ai-v2",
            explanation_category="normal",
            previous_state="ai_evaluated", new_state="scored")


def _restore_files(db: Session, storage) -> None:
    """Re-copy demo image files for existing rows (ephemeral disk hosts)."""
    from src.infrastructure.database.models import MediaAsset

    from demo_seed_social import WAVE_OWNERS

    demo_owners = sorted(
        {DEMO_USER_ID, *(c[1] for c in COMMUNITY), *WAVE_OWNERS})
    assets = (
        db.query(MediaAsset)
        .filter(MediaAsset.owner_user_id.in_(demo_owners))
        .all()
    )
    for asset in assets:
        source = _ASSETS / (asset.file_name or "")
        if not source.exists():
            continue
        if storage.read_original(asset.id) is None:
            storage.save_original(asset.id, source.read_bytes())
            try:
                storage.generate_derivative_stubs(asset.id)
            except FileNotFoundError:
                pass
