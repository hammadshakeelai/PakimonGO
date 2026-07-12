import uuid
from datetime import datetime, timezone

from sqlalchemy import BigInteger, Boolean, Column, DateTime, Float, ForeignKey, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


def _utcnow():
    return datetime.now(timezone.utc)


def _uuid():
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=_uuid)
    status = Column(String(32), default="active")
    age_band = Column(String(16), nullable=True)
    home_region = Column(String(8), nullable=True)
    trust_state = Column(String(32), default="neutral")
    created_at = Column(DateTime(timezone=True), default=_utcnow)
    updated_at = Column(DateTime(timezone=True), default=_utcnow, onupdate=_utcnow)
    deleted_at = Column(DateTime(timezone=True), nullable=True)


class MediaAsset(Base):
    __tablename__ = "media_assets"

    id = Column(String(36), primary_key=True, default=_uuid)
    owner_user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    file_name = Column(String(256))
    content_type = Column(String(64))
    byte_size = Column(BigInteger)
    sha256 = Column(String(64))
    storage_key = Column(String(512), nullable=True)
    asset_kind = Column(String(32), default="original")
    processing_state = Column(String(32), default="pending")
    created_at = Column(DateTime(timezone=True), default=_utcnow)
    updated_at = Column(DateTime(timezone=True), default=_utcnow, onupdate=_utcnow)


class MediaDerivative(Base):
    __tablename__ = "media_derivatives"

    id = Column(String(36), primary_key=True, default=_uuid)
    media_asset_id = Column(String(36), ForeignKey("media_assets.id"))
    size_label = Column(String(32))
    storage_key = Column(String(512))
    exif_stripped = Column(Boolean, default=False)
    visibility_state = Column(String(32), default="public")

    __table_args__ = (
        UniqueConstraint("media_asset_id", "size_label"),
    )


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(String(36), primary_key=True, default=_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    primary_media_asset_id = Column(String(36), ForeignKey("media_assets.id"))
    status = Column(String(32), default="pending")
    visibility = Column(String(16), default="private")
    submitted_at = Column(DateTime(timezone=True), default=_utcnow)
    created_at = Column(DateTime(timezone=True), default=_utcnow)
    updated_at = Column(DateTime(timezone=True), default=_utcnow, onupdate=_utcnow)

    media_asset = relationship("MediaAsset")
    capture_location = relationship("CaptureLocation", uselist=False)


class SubmissionAttribute(Base):
    __tablename__ = "submission_attributes"

    submission_id = Column(String(36), ForeignKey("submissions.id"), primary_key=True)
    animal_context = Column(String(16))
    real_name = Column(String(256))
    cute_name = Column(String(256))
    caption = Column(Text)
    tags = Column(Text, nullable=True)


class CaptureLocation(Base):
    __tablename__ = "capture_locations"

    submission_id = Column(String(36), ForeignKey("submissions.id"), primary_key=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    accuracy_meters = Column(Float, nullable=True)
    source = Column(String(32), default="gps")
    captured_at = Column(DateTime(timezone=True), default=_utcnow)
    submission = relationship("Submission", back_populates="capture_location")


class PublicLocationCell(Base):
    __tablename__ = "public_location_cells"

    id = Column(String(36), primary_key=True, default=_uuid)
    submission_id = Column(String(36), ForeignKey("submissions.id"))
    cell_id = Column(String(32))
    precision_label = Column(String(16), default="coarse")
    available_after = Column(DateTime(timezone=True), nullable=True)
    suppressed_reason = Column(String(64), nullable=True)


class SensitiveSpecies(Base):
    __tablename__ = "sensitive_species"

    id = Column(String(36), primary_key=True, default=_uuid)
    scientific_name = Column(String(256), unique=True, nullable=False)
    common_name = Column(String(256), nullable=True)
    suppression_level = Column(String(16), default="coarse_cell")
    reason = Column(String(256), nullable=True)
    created_at = Column(DateTime(timezone=True), default=_utcnow)


class ScoreEvent(Base):
    __tablename__ = "score_events"

    id = Column(String(36), primary_key=True, default=_uuid)
    submission_id = Column(String(36), ForeignKey("submissions.id"))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    ledger = Column(String(32))
    points = Column(Integer, nullable=True)
    event_type = Column(String(32))
    formula_version = Column(String(32), nullable=True)
    explanation_category = Column(String(32), nullable=True)
    previous_state = Column(String(32), nullable=True)
    new_state = Column(String(32))
    actor = Column(String(64), default="system")
    created_at = Column(DateTime(timezone=True), default=_utcnow)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(String(36), primary_key=True, default=_uuid)
    actor_user_id = Column(String(36), nullable=True)
    action = Column(String(64))
    target_type = Column(String(32))
    target_id = Column(String(36), nullable=True)
    metadata_json = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=_utcnow)


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(String(36), primary_key=True, default=_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    notification_type = Column(String(32), nullable=False)
    title = Column(String(256), nullable=False)
    body = Column(Text, nullable=True)
    reference_type = Column(String(32), nullable=True)
    reference_id = Column(String(36), nullable=True)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=_utcnow)


class Report(Base):
    __tablename__ = "reports"

    id = Column(String(36), primary_key=True, default=_uuid)
    reporter_user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    target_type = Column(String(16), nullable=False)  # "submission" | "user"
    target_id = Column(String(36), nullable=False, index=True)
    reason = Column(String(48), nullable=False)
    details = Column(Text, nullable=True)
    status = Column(String(16), default="open")  # open | reviewed | dismissed | actioned
    created_at = Column(DateTime(timezone=True), default=_utcnow)

    __table_args__ = (
        UniqueConstraint("reporter_user_id", "target_type", "target_id"),
    )


class Block(Base):
    __tablename__ = "blocks"

    id = Column(String(36), primary_key=True, default=_uuid)
    blocker_user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    blocked_user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=_utcnow)

    __table_args__ = (
        UniqueConstraint("blocker_user_id", "blocked_user_id"),
    )


class Reaction(Base):
    """One reaction per user per post; tapping the same kind again removes it."""

    __tablename__ = "reactions"

    id = Column(String(36), primary_key=True, default=_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    submission_id = Column(String(36), ForeignKey("submissions.id"), nullable=False, index=True)
    kind = Column(String(16), nullable=False)  # wow | cute | rare | safe_shot
    created_at = Column(DateTime(timezone=True), default=_utcnow)

    __table_args__ = (
        UniqueConstraint("user_id", "submission_id"),
    )


class Comment(Base):
    """Flat comments on a scored capture; soft-deleted via deleted_at."""

    __tablename__ = "comments"

    id = Column(String(36), primary_key=True, default=_uuid)
    submission_id = Column(String(36), ForeignKey("submissions.id"), nullable=False)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    body = Column(String(500), nullable=False)
    created_at = Column(DateTime(timezone=True), default=_utcnow)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        Index("ix_comments_submission_created", "submission_id", "created_at"),
    )


class Story(Base):
    """24-hour story; expiry is enforced by filtering expires_at > now."""

    __tablename__ = "stories"

    id = Column(String(36), primary_key=True, default=_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    media_asset_id = Column(String(36), ForeignKey("media_assets.id"), nullable=False)
    caption = Column(String(280), nullable=True)
    created_at = Column(DateTime(timezone=True), default=_utcnow)
    expires_at = Column(DateTime(timezone=True), nullable=False, index=True)

    __table_args__ = (
        Index("ix_stories_user_expires", "user_id", "expires_at"),
    )


class StoryView(Base):
    __tablename__ = "story_views"

    story_id = Column(String(36), ForeignKey("stories.id"), primary_key=True)
    viewer_id = Column(String(36), ForeignKey("users.id"), primary_key=True)
    viewed_at = Column(DateTime(timezone=True), default=_utcnow)


class Group(Base):
    """A wildlife community. Members share a feed, leaderboard, and roster."""

    __tablename__ = "groups"

    id = Column(String(36), primary_key=True, default=_uuid)
    name = Column(String(80), nullable=False)
    description = Column(String(280), nullable=True)
    cover_asset = Column(String(120), nullable=True)  # bundled dummy asset name
    is_public = Column(Boolean, default=True)
    created_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), default=_utcnow)


class GroupMember(Base):
    __tablename__ = "group_members"

    group_id = Column(String(36), ForeignKey("groups.id"), primary_key=True)
    user_id = Column(String(36), ForeignKey("users.id"), primary_key=True)
    role = Column(String(16), default="member")  # member | admin
    joined_at = Column(DateTime(timezone=True), default=_utcnow)

    __table_args__ = (
        Index("ix_group_members_user", "user_id", "group_id"),
    )


class Follow(Base):
    """Directed social-graph edge: follower_id follows followee_id."""

    __tablename__ = "follows"

    follower_id = Column(String(36), ForeignKey("users.id"), primary_key=True)
    followee_id = Column(String(36), ForeignKey("users.id"), primary_key=True)
    created_at = Column(DateTime(timezone=True), default=_utcnow)

    __table_args__ = (
        Index("ix_follows_followee", "followee_id", "follower_id"),
    )


class IdempotencyKey(Base):
    __tablename__ = "idempotency_keys"

    key = Column(String(128), primary_key=True)
    user_id = Column(String(36))
    operation = Column(String(64))
    request_hash = Column(String(64), nullable=True)
    response_ref = Column(String(256), nullable=True)
    expires_at = Column(DateTime(timezone=True))
