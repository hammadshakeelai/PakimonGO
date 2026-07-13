from __future__ import annotations

from sqlalchemy.orm import Session

from ..models import (
    CaptureLocation,
    ScoreEvent,
    SensitiveSpecies,
    Submission,
    SubmissionAttribute,
)


def get_public_sightings(
    db: Session,
    limit: int = 200,
    blocked: set[str] | None = None,
) -> list[dict]:
    """Community sightings for the living map: PUBLIC scored captures
    only, coarse ~1km cells (2-decimal rounding — never the exact GPS),
    sensitive species and blocked users excluded.

    Payload mirrors the submission-list marker shape so the mobile
    ``SubmissionMarker.fromJson`` parses it unchanged.
    """
    sensitive_subq = (
        db.query(SensitiveSpecies.scientific_name)
        .filter(SensitiveSpecies.scientific_name.ilike(SubmissionAttribute.real_name))
        .exists()
    )
    query = (
        db.query(
            Submission.id,
            Submission.user_id,
            Submission.primary_media_asset_id,
            Submission.status,
            Submission.created_at,
            SubmissionAttribute.real_name,
            ScoreEvent.points,
            CaptureLocation.latitude,
            CaptureLocation.longitude,
        )
        .select_from(Submission)
        .join(SubmissionAttribute, SubmissionAttribute.submission_id == Submission.id)
        .join(ScoreEvent, ScoreEvent.submission_id == Submission.id)
        .join(CaptureLocation, CaptureLocation.submission_id == Submission.id)
        .filter(
            Submission.visibility == "public",
            Submission.status.in_(["scored", "capped"]),
            ScoreEvent.points.isnot(None),
            ~sensitive_subq,
        )
        .order_by(Submission.created_at.desc())
    )
    if blocked:
        query = query.filter(~Submission.user_id.in_(blocked))

    items: list[dict] = []
    seen: set[str] = set()
    for row in query.limit(limit * 2).all():  # headroom for dedupe
        if row.id in seen:
            continue
        seen.add(row.id)
        cell_lat = round(row.latitude, 2)
        cell_lng = round(row.longitude, 2)
        items.append(
            {
                "submissionId": row.id,
                "userId": row.user_id,
                "mediaAssetId": row.primary_media_asset_id,
                "species": row.real_name,
                "status": row.status,
                "scoreEvent": {"points": row.points},
                "publicLocation": {
                    "cellId": f"cell_{cell_lat:.2f}_{cell_lng:.2f}",
                    "cellLatitude": cell_lat,
                    "cellLongitude": cell_lng,
                },
                "createdAt": row.created_at.isoformat() if row.created_at else None,
            }
        )
        if len(items) >= limit:
            break
    return items
