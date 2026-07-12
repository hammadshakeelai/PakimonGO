"""Expanded demo content: a second wave of posts on new species photos,
four more community photographers, a realistic follow graph (with the
follow notifications a real follow would create), and extra comments and
reactions. Keeps the Following feed and Friends leaderboard populated
for any demo account out of the box.

Idempotent: each section checks for existing rows before inserting.
"""

from __future__ import annotations

import logging

from sqlalchemy.orm import Session

log = logging.getLogger("demo_seed")

# Four more photographers, each with a themed set of captures. Uses only
# images not already claimed by WAVE (each photo backs one post).
# (file, owner, scientific, cute, points, lat, lng, caption)
WAVE2 = [
    ("black_kite.jpg", "lens_farah", "Milvus migrans", "Cheel", 45,
     33.7212, 73.0605, "Black kite wheeling over the F-9 canopy."),
    ("indian_roller.jpg", "lens_farah", "Coracias benghalensis", "Neelkanth", 55,
     33.7099, 73.0788, "Indian roller flashing that impossible blue."),
    ("green_bee_eater.jpg", "lens_farah", "Merops orientalis", "Zumurrud", 50,
     33.6981, 73.0512, "Bee-eater lining up a snack on the wire."),
    ("common_kingfisher.jpg", "trekker_usman", "Alcedo atthis", "Chamak", 60,
     33.7488, 73.1301, "Common kingfisher, tiny jewel of the stream."),
    ("shikra.jpg", "trekker_usman", "Accipiter badius", "Baaz", 65,
     33.7602, 73.1188, "Shikra scanning the trail-5 undergrowth."),
    ("monitor_lizard.jpg", "trekker_usman", "Varanus bengalensis", "Goh", 50,
     33.7550, 73.1055, "Bengal monitor sunning on the rocks. Gave it space."),
    ("little_egret.jpg", "birder_nadia", "Egretta garzetta", "Nanhi", 40,
     33.6805, 73.1210, "Little egret dancing for fish at dawn."),
    ("painted_stork.jpg", "birder_nadia", "Mycteria leucocephala", "Rangeen", 70,
     33.6700, 73.1322, "Painted storks stopped over at the wetland!"),
    ("cattle_egret.jpg", "birder_nadia", "Bubulcus ibis", "Bagla", 30,
     33.6759, 73.1150, "Cattle egrets shadowing the buffalo herd."),
    ("jungle_babbler.jpg", "birder_nadia", "Argya striata", "Saat-Bhai", 25,
     33.6902, 73.0933, "The seven sisters, squabbling as always."),
    ("black_drongo.jpg", "wildpk_kamran", "Dicrurus macrocercus", "Kotwal", 35,
     33.7002, 73.0450, "King crow owning the fence line at golden hour."),
    ("koel.jpg", "wildpk_kamran", "Eudynamys scolopaceus", "Koyal", 30,
     33.7301, 73.0910, "Heard the koel all summer — finally saw it."),
    ("red_wattled_lapwing.jpg", "wildpk_kamran", "Vanellus indicus", "Titeeri", 35,
     33.7410, 73.0966, "Did-he-do-it calling across the mudflat."),
]

WAVE2_OWNERS = sorted({row[1] for row in WAVE2})

# Follow edges (follower -> followee) weaving the whole demo cast together.
FOLLOW_GRAPH = [
    ("pakimongo_official", "ranger_bilal"),
    ("pakimongo_official", "shutter_zara"),
    ("pakimongo_official", "birder_nadia"),
    ("ranger_bilal", "pakimongo_official"),
    ("ranger_bilal", "trekker_usman"),
    ("ranger_bilal", "wetland_watch"),
    ("shutter_zara", "pakimongo_official"),
    ("shutter_zara", "lens_farah"),
    ("shutter_zara", "birder_nadia"),
    ("lens_farah", "shutter_zara"),
    ("lens_farah", "wildpk_kamran"),
    ("lens_farah", "pakimongo_official"),
    ("trekker_usman", "ranger_bilal"),
    ("trekker_usman", "margalla_hiker"),
    ("birder_nadia", "wetland_watch"),
    ("birder_nadia", "shutter_zara"),
    ("birder_nadia", "lens_farah"),
    ("wildpk_kamran", "citylights_ali"),
    ("wildpk_kamran", "pakimongo_official"),
    ("margalla_hiker", "trekker_usman"),
    ("margalla_hiker", "ranger_bilal"),
    ("wetland_watch", "birder_nadia"),
    ("citylights_ali", "wildpk_kamran"),
    ("trailcam_omar", "ranger_bilal"),
    ("wildlens_aisha", "shutter_zara"),
    ("safeshot_sara", "pakimongo_official"),
    ("birdnerd_hina", "lens_farah"),
]

# (post file, commenter, body)
COMMENTS2 = [
    ("indian_roller.jpg", "shutter_zara", "That blue is unreal — perfect light."),
    ("indian_roller.jpg", "birder_nadia", "Roller shots are so hard, well done!"),
    ("painted_stork.jpg", "wetland_watch", "Painted storks here?! Bucket-list record."),
    ("painted_stork.jpg", "lens_farah", "Okay I need to visit that wetland."),
    ("shikra.jpg", "ranger_bilal", "Sharp eyes catching a shikra on trail 5."),
    ("common_kingfisher.jpg", "wildpk_kamran", "Tiny jewel indeed. Stunning."),
    ("monitor_lizard.jpg", "margalla_hiker", "Gave it space — respect. Great capture."),
    ("black_kite.jpg", "trekker_usman", "F-9 kites are the best free air show."),
    ("green_bee_eater.jpg", "birdnerd_hina", "Bee-eaters never miss. Gorgeous."),
    ("koel.jpg", "pakimongo_official", "That call haunted my whole summer!"),
]

# (post file, reactor, kind)
REACTIONS2 = [
    ("indian_roller.jpg", "shutter_zara", "wow"),
    ("indian_roller.jpg", "pakimongo_official", "rare"),
    ("indian_roller.jpg", "birder_nadia", "wow"),
    ("painted_stork.jpg", "wetland_watch", "rare"),
    ("painted_stork.jpg", "lens_farah", "wow"),
    ("painted_stork.jpg", "ranger_bilal", "rare"),
    ("shikra.jpg", "trekker_usman", "safe_shot"),
    ("shikra.jpg", "margalla_hiker", "wow"),
    ("common_kingfisher.jpg", "wildpk_kamran", "cute"),
    ("common_kingfisher.jpg", "shutter_zara", "wow"),
    ("green_bee_eater.jpg", "lens_farah", "cute"),
    ("monitor_lizard.jpg", "ranger_bilal", "safe_shot"),
    ("black_kite.jpg", "citylights_ali", "wow"),
    ("koel.jpg", "birdnerd_hina", "cute"),
    ("little_egret.jpg", "wetland_watch", "cute"),
    ("cattle_egret.jpg", "safeshot_sara", "wow"),
]


# Groups: (name, description, cover_asset, [member owners])
GROUPS = [
    (
        "Islamabad Wildlife Squad",
        "Capturing the birds and beasts of the capital — safely.",
        "markhor.jpg",
        ["pakimongo_official", "ranger_bilal", "shutter_zara", "birder_nadia",
         "lens_farah", "trekker_usman", "wildpk_kamran", "margalla_hiker",
         "wetland_watch", "citylights_ali"],
    ),
    (
        "Margalla Trail Trackers",
        "Ridge hikers logging mammals and raptors on the Margalla trails.",
        "golden_eagle.jpg",
        ["ranger_bilal", "trekker_usman", "margalla_hiker", "shutter_zara"],
    ),
    (
        "Rawal Lake Birders",
        "Waterbirds, kingfishers, and wetland watch at Rawal Lake.",
        "white_throated_kingfisher.jpg",
        ["wetland_watch", "birder_nadia", "shutter_zara", "lens_farah",
         "pakimongo_official"],
    ),
]


def seed_graph_and_wave2(db: Session, storage) -> None:
    """Second wave of posts + follow graph + groups + extra social content."""
    from demo_seed_social import (
        _seed_comments_reactions_from,
        _seed_wave_captures,
    )

    _seed_wave_captures(db, storage, WAVE2)
    _seed_comments_reactions_from(db, COMMENTS2, REACTIONS2)
    _seed_follow_graph(db)
    _seed_groups(db)


def _seed_groups(db: Session) -> None:
    """Create demo groups and memberships (idempotent by group name)."""
    from src.infrastructure.database.repositories.group import (
        add_member,
        create_group,
        get_group_by_name,
    )

    for name, desc, cover, members in GROUPS:
        group = get_group_by_name(db, name)
        if group is None:
            group = create_group(
                db, name, description=desc, cover_asset=cover,
                created_by=members[0] if members else None)
        for i, owner in enumerate(members):
            add_member(db, group.id, owner, role="admin" if i == 0 else "member")


def _seed_follow_graph(db: Session) -> None:
    """Create follow edges + the follow notifications a real follow makes."""
    from src.infrastructure.database.models import User
    from src.infrastructure.database.repositories import (
        create_notification,
        follow_user,
        is_following,
    )

    for follower, followee in FOLLOW_GRAPH:
        # Both users must exist (waves seed them); skip otherwise.
        if db.query(User.id).filter(User.id == follower).first() is None:
            continue
        if db.query(User.id).filter(User.id == followee).first() is None:
            continue
        if is_following(db, follower, followee):
            continue
        follow_user(db, follower, followee)
        create_notification(
            db,
            user_id=followee,
            notification_type="new_follower",
            title="New follower",
            body=f"{follower} started following you.",
            reference_type="user",
            reference_id=follower,
        )
