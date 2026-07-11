"""Social wave of demo content: real CC-licensed wildlife photos
(assets/demo/wild/, see CREDITS.md), six more community accounts,
comments, reactions, and self-refreshing 24h stories.

Idempotent: capture rows are seeded once per owner; stories are
re-created on boot whenever a storyteller has none active, so the demo
ring never goes empty on production.
"""

from __future__ import annotations

import hashlib
import logging
from datetime import datetime, timedelta, timezone
from pathlib import Path

from sqlalchemy.orm import Session

log = logging.getLogger("demo_seed")

_WILD = Path(__file__).resolve().parents[1] / "assets" / "demo" / "wild"

# (file, owner, scientific name, cute name, points, lat, lng, caption)
WAVE = [
    ("house_sparrow.jpg", "birdnerd_hina", "Passer domesticus", "Chota", 25,
     33.7180, 73.0620, "The bravest sparrow at Fatima Jinnah Park."),
    ("hoopoe.jpg", "birdnerd_hina", "Upupa epops", "Crown", 45,
     33.7052, 73.0895, "A hoopoe drumming the lawn for grubs — crest up!"),
    ("rose_ringed_parakeet.jpg", "birdnerd_hina", "Psittacula krameri", "Mithu", 30,
     33.7099, 73.0555, "Parakeet raid on the guava tree, as loud as ever."),
    ("markhor.jpg", "ranger_bilal", "Capra falconeri", "Sardar", 80,
     33.7488, 73.1450, "Markhor on the ridge — Pakistan's national animal, wild and free."),
    ("golden_eagle.jpg", "ranger_bilal", "Aquila chrysaetos", "Shaheen", 75,
     33.7601, 73.1200, "Golden eagle circling trail 5 thermals."),
    ("red_fox.jpg", "ranger_bilal", "Vulpes vulpes", "Lomri", 55,
     33.7702, 73.0998, "Red fox at dusk, kept my distance and my breath."),
    ("white_throated_kingfisher.jpg", "shutter_zara", "Halcyon smyrnensis", "Neelam", 60,
     33.7301, 73.0977, "White-throated kingfisher owning the Rawal shoreline."),
    ("peacock_butterfly.jpg", "shutter_zara", "Aglais io", "Rani", 35,
     33.6989, 73.0701, "Peacock butterfly sunning on the trail bricks."),
    ("spotted_owlet.jpg", "shutter_zara", "Athene brama", "Chashmish", 50,
     33.6902, 73.0533, "Spotted owlet judging me from the neem tree."),
    ("great_egret.jpg", "wetland_watch", "Ardea alba", "Safed", 40,
     33.6805, 73.1188, "Great egret statue-still in the shallows."),
    ("greater_flamingo.jpg", "wetland_watch", "Phoenicopterus roseus", "Gulabi", 65,
     33.6700, 73.1302, "Flamingos passing through — wetlands worth protecting."),
    ("grey_heron.jpg", "wetland_watch", "Ardea cinerea", "Dhairya", 40,
     33.6759, 73.1250, "Grey heron on patrol at first light."),
    ("indian_flapshell_turtle.jpg", "wetland_watch", "Lissemys punctata", "Kachwa", 55,
     33.6811, 73.1099, "Flapshell turtle basking — logged and left undisturbed."),
    ("gray_langur.jpg", "margalla_hiker", "Semnopithecus entellus", "Bandar", 50,
     33.7555, 73.0888, "Langur troop escort on the Margalla trail."),
    ("chital_deer.jpg", "margalla_hiker", "Axis axis", "Heeral", 60,
     33.7620, 73.0790, "Chital stag stepped out of the mist. Unreal morning."),
    ("common_myna.jpg", "citylights_ali", "Acridotheres tristis", "Sheda", 20,
     33.7002, 73.0450, "Mynas run this block, I just live here."),
    ("house_crow.jpg", "citylights_ali", "Corvus splendens", "Kaala", 20,
     33.6955, 73.0388, "Smartest bird on the street, change my mind."),
]

# Storytellers whose ring should always have something live.
STORY_ROTATION = [
    ("pakimongo_official", "Scouting new trails today 🌿"),
    ("ranger_bilal", "Markhor country. Keep your distance, keep them wild."),
    ("shutter_zara", "Golden hour at Rawal Lake."),
    ("wetland_watch", "Counting egrets before breakfast."),
]

# (owner of post file, commenter, body)
COMMENTS = [
    ("markhor.jpg", "birdnerd_hina", "Incredible sighting — how far up were you?"),
    ("markhor.jpg", "wildlens_aisha", "National animal looking majestic 🔥"),
    ("markhor.jpg", "safeshot_sara", "Respectful distance too. Model capture."),
    ("golden_eagle.jpg", "trailcam_omar", "That wingspan! Trail 5 never disappoints."),
    ("white_throated_kingfisher.jpg", "citylights_ali", "The colors on this one are unreal."),
    ("white_throated_kingfisher.jpg", "birdnerd_hina", "Kingfisher supremacy 💙"),
    ("spotted_owlet.jpg", "margalla_hiker", "It's definitely judging you 😂"),
    ("greater_flamingo.jpg", "shutter_zara", "Wait, flamingos HERE? Amazing record."),
    ("chital_deer.jpg", "wetland_watch", "Misty mornings give the best captures."),
    ("hoopoe.jpg", "ranger_bilal", "Crest fully up — great timing."),
]

# (post file, reactor, kind)
REACTIONS = [
    ("markhor.jpg", "birdnerd_hina", "wow"),
    ("markhor.jpg", "wildlens_aisha", "rare"),
    ("markhor.jpg", "trailcam_omar", "wow"),
    ("markhor.jpg", "safeshot_sara", "safe_shot"),
    ("golden_eagle.jpg", "shutter_zara", "wow"),
    ("golden_eagle.jpg", "citylights_ali", "rare"),
    ("white_throated_kingfisher.jpg", "birdnerd_hina", "cute"),
    ("white_throated_kingfisher.jpg", "margalla_hiker", "wow"),
    ("spotted_owlet.jpg", "shutter_zara", "cute"),
    ("spotted_owlet.jpg", "wetland_watch", "cute"),
    ("greater_flamingo.jpg", "ranger_bilal", "rare"),
    ("chital_deer.jpg", "birdnerd_hina", "wow"),
    ("hoopoe.jpg", "safeshot_sara", "safe_shot"),
    ("red_fox.jpg", "wildlens_aisha", "rare"),
    ("indian_flapshell_turtle.jpg", "trailcam_omar", "safe_shot"),
]

WAVE_OWNERS = sorted({row[1] for row in WAVE})


def seed_social_wave(db: Session, storage) -> None:
    """Seed the wave captures, comments, reactions, and refresh stories."""
    if not _WILD.exists():
        log.warning("wild demo assets missing: %s", _WILD)
        return
    _seed_captures(db, storage)
    _seed_comments_reactions(db)
    _refresh_stories(db)


def _asset_for_file(db: Session, file_name: str):
    from src.infrastructure.database.models import MediaAsset

    return (
        db.query(MediaAsset)
        .filter(MediaAsset.file_name == f"wild/{file_name}")
        .first()
    )


def _submission_for_file(db: Session, file_name: str):
    from src.infrastructure.database.models import Submission

    asset = _asset_for_file(db, file_name)
    if asset is None:
        return None
    return (
        db.query(Submission)
        .filter(Submission.primary_media_asset_id == asset.id)
        .first()
    )


def _seed_captures(db: Session, storage) -> None:
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
        create_score_event,
        update_submission_status,
    )

    seeded_owners = set()
    for file_name, owner, species, cute, points, lat, lng, caption in WAVE:
        if owner not in seeded_owners:
            if db.query(User).filter(User.id == owner).first() is not None:
                seeded_owners.add(owner)
            else:
                db.add(User(id=owner, trust_state="verified",
                            age_band="adult", home_region="PK"))
                db.commit()
                seeded_owners.add(owner)
        if _asset_for_file(db, file_name) is not None:
            continue  # this capture already exists
        source = _WILD / file_name
        if not source.exists():
            continue
        content = source.read_bytes()
        sha = hashlib.sha256(content + owner.encode()).hexdigest()
        asset = create_media_asset(
            db, f"wild/{file_name}", "image/jpeg", len(content), sha,
            owner_user_id=owner)
        storage.save_original(asset.id, content)
        storage.generate_derivative_stubs(asset.id)
        complete_media_asset(db, asset.id, sha)
        sub = Submission(user_id=owner, primary_media_asset_id=asset.id,
                         status="scored", visibility="private")
        db.add(sub)
        db.flush()
        db.add(SubmissionAttribute(
            submission_id=sub.id, animal_context="wild", real_name=species,
            cute_name=cute, caption=caption, tags="wild"))
        db.add(CaptureLocation(submission_id=sub.id, latitude=lat,
                               longitude=lng, accuracy_meters=15.0, source="gps"))
        db.add(PublicLocationCell(
            submission_id=sub.id,
            cell_id=f"cell_{round(lat, 2):.2f}_{round(lng, 2):.2f}",
            precision_label="cell"))
        db.commit()
        update_submission_status(db, sub.id, "scored")
        create_score_event(
            db=db, submission_id=sub.id, user_id=owner, ledger="wild",
            points=points, event_type="scored", formula_version="ai-v2",
            explanation_category="normal",
            previous_state="ai_evaluated", new_state="scored")


def _seed_comments_reactions(db: Session) -> None:
    from src.infrastructure.database.models import Comment, Reaction

    for file_name, commenter, body in COMMENTS:
        sub = _submission_for_file(db, file_name)
        if sub is None:
            continue
        exists = (
            db.query(Comment)
            .filter(Comment.submission_id == sub.id,
                    Comment.user_id == commenter,
                    Comment.body == body)
            .first()
        )
        if exists is None:
            db.add(Comment(submission_id=sub.id, user_id=commenter, body=body))
    for file_name, reactor, kind in REACTIONS:
        sub = _submission_for_file(db, file_name)
        if sub is None:
            continue
        exists = (
            db.query(Reaction)
            .filter(Reaction.submission_id == sub.id,
                    Reaction.user_id == reactor)
            .first()
        )
        if exists is None:
            db.add(Reaction(submission_id=sub.id, user_id=reactor, kind=kind))
    db.commit()


def _refresh_stories(db: Session) -> None:
    """Keep the demo story ring alive: each storyteller always has one
    active story (their most recent capture photo)."""
    from src.infrastructure.database.models import MediaAsset, Story

    now = datetime.now(timezone.utc)
    for owner, caption in STORY_ROTATION:
        active = (
            db.query(Story)
            .filter(Story.user_id == owner, Story.expires_at > now)
            .first()
        )
        if active is not None:
            continue
        asset = (
            db.query(MediaAsset)
            .filter(MediaAsset.owner_user_id == owner)
            .order_by(MediaAsset.created_at.desc())
            .first()
        )
        if asset is None:
            continue
        db.add(Story(user_id=owner, media_asset_id=asset.id, caption=caption,
                     expires_at=now + timedelta(hours=24)))
    db.commit()
