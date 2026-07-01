
from sqlalchemy.orm import Session

from ..models import SensitiveSpecies


def is_sensitive_species(db: Session, scientific_name: str) -> bool:
    return (
        db.query(SensitiveSpecies)
        .filter(SensitiveSpecies.scientific_name.ilike(scientific_name))
        .first()
        is not None
    )


def get_or_create_sensitive_species(
    db: Session,
    scientific_name: str,
    common_name: str | None = None,
    suppression_level: str = "coarse_cell",
    reason: str | None = None,
) -> "SensitiveSpecies":
    species = (
        db.query(SensitiveSpecies)
        .filter(SensitiveSpecies.scientific_name.ilike(scientific_name))
        .first()
    )
    if species:
        return species
    return create_sensitive_species(db, scientific_name, common_name, suppression_level, reason)


def get_sensitive_species(db: Session) -> list[dict]:
    rows = db.query(SensitiveSpecies).all()
    return [
        {
            "scientificName": row.scientific_name,
            "commonName": row.common_name,
            "suppressionLevel": row.suppression_level,
            "reason": row.reason,
        }
        for row in rows
    ]


def create_sensitive_species(
    db: Session,
    scientific_name: str,
    common_name: str | None = None,
    suppression_level: str = "coarse_cell",
    reason: str | None = None,
) -> "SensitiveSpecies":
    species = SensitiveSpecies(
        scientific_name=scientific_name,
        common_name=common_name,
        suppression_level=suppression_level,
        reason=reason,
    )
    db.add(species)
    db.commit()
    db.refresh(species)
    return species
