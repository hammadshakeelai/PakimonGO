"""Social-layer models: reactions, comments, stories, follows, groups,
and group quests. Split from models.py to keep both under the 300-line
rule; models.py re-exports everything here, so importing from
``..models`` keeps working everywhere.
"""

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Index, Integer, String, UniqueConstraint

from .models import Base, _utcnow, _uuid


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


class CommentLike(Base):
    """Heart on a comment; one per user per comment (tap again removes)."""

    __tablename__ = "comment_likes"

    comment_id = Column(String(36), ForeignKey("comments.id"), primary_key=True)
    user_id = Column(String(36), ForeignKey("users.id"), primary_key=True)
    created_at = Column(DateTime(timezone=True), default=_utcnow)


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


class StoryReaction(Base):
    """Quick emoji reaction to a story; one per viewer per story
    (re-reacting replaces the emoji)."""

    __tablename__ = "story_reactions"

    story_id = Column(String(36), ForeignKey("stories.id"), primary_key=True)
    viewer_id = Column(String(36), ForeignKey("users.id"), primary_key=True)
    emoji = Column(String(16), nullable=False)  # heart | fire | wow | clap
    created_at = Column(DateTime(timezone=True), default=_utcnow)


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


class GroupQuest(Base):
    """Time-boxed community challenge; progress is computed live from
    members' scored captures inside the quest window."""

    __tablename__ = "group_quests"

    id = Column(String(36), primary_key=True, default=_uuid)
    group_id = Column(String(36), ForeignKey("groups.id"), nullable=False, index=True)
    title = Column(String(120), nullable=False)
    description = Column(String(280), nullable=True)
    kind = Column(String(16), default="captures")  # captures | species | points
    target = Column(Integer, nullable=False)
    starts_at = Column(DateTime(timezone=True), default=_utcnow)
    ends_at = Column(DateTime(timezone=True), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), default=_utcnow)


class Follow(Base):
    """Directed social-graph edge: follower_id follows followee_id."""

    __tablename__ = "follows"

    follower_id = Column(String(36), ForeignKey("users.id"), primary_key=True)
    followee_id = Column(String(36), ForeignKey("users.id"), primary_key=True)
    created_at = Column(DateTime(timezone=True), default=_utcnow)

    __table_args__ = (
        Index("ix_follows_followee", "followee_id", "follower_id"),
    )
