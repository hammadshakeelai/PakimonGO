from datetime import datetime, timezone

from src.infrastructure.database.models import (
    Base, CaptureLocation, MediaAsset, Notification, PublicLocationCell,
    ScoreEvent, Submission, SubmissionAttribute, User,
)
from src.infrastructure.database.session import get_engine, get_session_local


def _utcnow():
    return datetime.now(timezone.utc)


SEED_USERS = [
    {"id": "seed_user_alpha", "age_band": "18_24", "home_region": "PK"},
    {"id": "seed_user_beta", "age_band": "25_34", "home_region": "IN"},
]

SEED_SPECIES = [
    {"real_name": "Markhor", "context": "wild", "points": 75, "lat": 33.7, "lng": 73.1},
    {"real_name": "Snow Leopard", "context": "wild", "points": 100, "lat": 35.9, "lng": 74.8},
    {"real_name": "Peacock", "context": "zoo", "points": 5, "lat": 33.6, "lng": 73.0},
    {"real_name": "Indian Rhinoceros", "context": "zoo", "points": 3, "lat": 26.5, "lng": 80.2},
    {"real_name": "Golden Eagle", "context": "wild", "points": 50, "lat": 34.0, "lng": 73.5},
    {"real_name": "Bengal Tiger", "context": "zoo", "points": 10, "lat": 27.5, "lng": 77.7},
]


def seed_database():
    engine = get_engine()
    Base.metadata.create_all(bind=engine)
    db = get_session_local()()

    try:
        existing = db.query(User).count()
        if existing > 0:
            print(f"Database already has {existing} users — skipping seed.")
            return

        users = []
        for u in SEED_USERS:
            user = User(**u, trust_state="verified")
            db.add(user)
            users.append(user)
        db.flush()

        for i, s in enumerate(SEED_SPECIES):
            user = users[i % len(users)]

            media = MediaAsset(
                id=f"seed_media_{i}",
                owner_user_id=user.id,
                file_name=f"{s['real_name'].lower().replace(' ', '_')}.jpg",
                content_type="image/jpeg",
                byte_size=102400,
                sha256=f"seed_sha256_{i}",
                processing_state="completed",
            )
            db.add(media)
            db.flush()

            status = "scored" if s["context"] == "zoo" else "ai_evaluated"

            sub = Submission(
                id=f"seed_sub_{i}",
                user_id=user.id,
                primary_media_asset_id=media.id,
                status=status,
                visibility="public",
                submitted_at=_utcnow(),
            )
            db.add(sub)
            db.flush()

            attr = SubmissionAttribute(
                submission_id=sub.id,
                animal_context=s["context"],
                real_name=s["real_name"],
                cute_name=s["real_name"],
                caption=f"A beautiful {s['real_name']} spotted in the wild!",
            )
            db.add(attr)

            loc = CaptureLocation(
                submission_id=sub.id,
                latitude=s["lat"],
                longitude=s["lng"],
                accuracy_meters=50.0,
            )
            db.add(loc)

            pub = PublicLocationCell(
                submission_id=sub.id,
                cell_id=f"cell_{s['lat']:.2f}_{s['lng']:.2f}",
                precision_label="cell",
            )
            db.add(pub)

            score = ScoreEvent(
                submission_id=sub.id,
                user_id=user.id,
                ledger=s["context"],
                points=s["points"],
                event_type="final",
                formula_version="v1",
                explanation_category=s["context"],
                new_state=status,
                actor="system",
            )
            db.add(score)

            notif = Notification(
                user_id=user.id,
                notification_type="score",
                title=f"{s['real_name']} Scored!",
                body=f"Your {s['real_name']} earned {s['points']} points",
                reference_type="submission",
                reference_id=sub.id,
                is_read=False,
            )
            db.add(notif)

        db.commit()
        print(f"Seeded {len(SEED_USERS)} users, {len(SEED_SPECIES)} submissions.")

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
