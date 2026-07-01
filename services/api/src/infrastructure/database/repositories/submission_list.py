
from sqlalchemy.orm import Session

from ..models import ScoreEvent, SensitiveSpecies, Submission, SubmissionAttribute


def get_submissions(
    db: Session,
    user_id: str | None = None,
    limit: int = 20,
    offset: int = 0,
    status: str | None = None,
    animal_context: str | None = None,
    sort_by: str = "createdAt",
    sort_order: str = "desc",
    include_sensitive: bool = False,
) -> tuple[list[dict], int]:

    query = (
        db.query(
            Submission.id,
            Submission.user_id,
            Submission.primary_media_asset_id,
            Submission.status,
            Submission.submitted_at,
            Submission.created_at,
            SubmissionAttribute.real_name,
            SubmissionAttribute.animal_context,
            SubmissionAttribute.cute_name,
            SubmissionAttribute.caption,
            ScoreEvent.points,
            ScoreEvent.ledger,
            ScoreEvent.explanation_category,
        )
        .select_from(Submission)
        .join(SubmissionAttribute, SubmissionAttribute.submission_id == Submission.id, isouter=True)
        .join(ScoreEvent, ScoreEvent.submission_id == Submission.id, isouter=True)
    )

    if user_id:
        query = query.filter(Submission.user_id == user_id)
    if status:
        query = query.filter(Submission.status == status)
    if animal_context:
        query = query.filter(SubmissionAttribute.animal_context == animal_context)
    if not include_sensitive:
        sensitive_subq = (
            db.query(SensitiveSpecies.scientific_name)
            .filter(SensitiveSpecies.scientific_name.ilike(SubmissionAttribute.real_name))
            .exists()
        )
        query = query.filter(~sensitive_subq)

    total = query.count()

    sort_column = {
        "createdAt": Submission.created_at,
        "submittedAt": Submission.submitted_at,
        "status": Submission.status,
        "points": ScoreEvent.points,
        "species": SubmissionAttribute.real_name,
    }.get(sort_by, Submission.created_at)

    if sort_order == "asc":
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    rows = query.limit(limit).offset(offset).all()

    items = []
    for row in rows:
        score_event = None
        if row.points is not None:
            score_event = {
                "points": row.points,
                "ledger": row.ledger,
                "explanation": row.explanation_category,
            }
        items.append(
            {
                "submissionId": row.id,
                "userId": row.user_id,
                "mediaAssetId": row.primary_media_asset_id,
                "status": row.status,
                "submittedAt": row.submitted_at.isoformat() if row.submitted_at else None,
                "createdAt": row.created_at.isoformat() if row.created_at else None,
                "species": row.real_name,
                "context": row.animal_context,
                "cuteName": row.cute_name,
                "caption": row.caption,
                "scoreEvent": score_event,
            }
        )
    return items, total
