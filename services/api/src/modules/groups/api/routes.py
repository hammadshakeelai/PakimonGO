from __future__ import annotations

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from src.infrastructure.auth.adapter import UserContext
from src.infrastructure.auth.dependencies import get_current_user
from src.infrastructure.database.repositories import (
    get_blocked_user_ids,
    get_group,
    get_leaderboard,
    get_or_create_user,
    group_member_ids,
    join_group,
    leave_group,
    list_group_quests,
    list_groups,
    list_members,
)
from src.infrastructure.database.repositories.group import (
    add_member,
    create_group,
    get_group_by_name,
)
from src.infrastructure.database.session import get_db
from src.infrastructure.middleware.rate_limit import allow
from src.modules.feed.api.routes import build_feed_page

router = APIRouter(prefix="/groups", tags=["groups"])

MIN_NAME_LEN = 3
MAX_NAME_LEN = 80
MAX_DESC_LEN = 280
GROUPS_PER_DAY = 5


@router.get("")
def list_all(
    db: Session = Depends(get_db),
    user: UserContext = Depends(get_current_user),
) -> dict:
    """All wildlife groups with membership + counts for the caller."""
    groups = list_groups(db, user.user_id)
    return {"items": groups, "total": len(groups)}


@router.post("", status_code=201)
def create(
    payload: dict = Body(...),
    db: Session = Depends(get_db),
    user: UserContext = Depends(get_current_user),
) -> dict:
    """Start a new wildlife community; the creator becomes its admin."""
    name = (payload.get("name") or "").strip()
    description = payload.get("description")
    if not (MIN_NAME_LEN <= len(name) <= MAX_NAME_LEN):
        raise HTTPException(
            status_code=400,
            detail=f"name must be {MIN_NAME_LEN}-{MAX_NAME_LEN} characters",
        )
    if description is not None and (
        not isinstance(description, str) or len(description) > MAX_DESC_LEN
    ):
        raise HTTPException(
            status_code=400,
            detail=f"description must be at most {MAX_DESC_LEN} chars",
        )
    if get_group_by_name(db, name) is not None:
        raise HTTPException(
            status_code=409, detail="A group with this name already exists")
    if not allow(f"groupcreate:{user.user_id}", GROUPS_PER_DAY, 86400.0):
        raise HTTPException(
            status_code=429, detail="Too many new groups — try again tomorrow")
    get_or_create_user(db, user.user_id)  # first action may be group creation
    group = create_group(
        db, name, description=description, created_by=user.user_id)
    add_member(db, group.id, user.user_id, role="admin")
    return get_group(db, group.id, user.user_id)


@router.get("/{group_id}")
def detail(
    group_id: str,
    db: Session = Depends(get_db),
    user: UserContext = Depends(get_current_user),
) -> dict:
    group = get_group(db, group_id, user.user_id)
    if group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return group


@router.post("/{group_id}/join", status_code=201)
def join(
    group_id: str,
    db: Session = Depends(get_db),
    user: UserContext = Depends(get_current_user),
) -> dict:
    if not join_group(db, group_id, user.user_id):
        raise HTTPException(status_code=404, detail="Group not found")
    return {"status": "ok", "groupId": group_id, "isMember": True}


@router.delete("/{group_id}/join")
def leave(
    group_id: str,
    db: Session = Depends(get_db),
    user: UserContext = Depends(get_current_user),
) -> dict:
    if not leave_group(db, group_id, user.user_id):
        raise HTTPException(status_code=404, detail="You are not a member")
    return {"status": "ok", "groupId": group_id, "isMember": False}


@router.get("/{group_id}/members")
def members(
    group_id: str,
    db: Session = Depends(get_db),
    user: UserContext = Depends(get_current_user),
) -> dict:
    if get_group(db, group_id, user.user_id) is None:
        raise HTTPException(status_code=404, detail="Group not found")
    ids = list_members(db, group_id)
    return {"items": ids, "total": len(ids)}


@router.get("/{group_id}/leaderboard")
def group_leaderboard(
    group_id: str,
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
    user: UserContext = Depends(get_current_user),
) -> dict:
    """Members ranked by points (reuses the global leaderboard, scoped to
    this group's roster)."""
    if get_group(db, group_id, user.user_id) is None:
        raise HTTPException(status_code=404, detail="Group not found")
    members_ids = group_member_ids(db, group_id)
    entries, total = get_leaderboard(
        db=db,
        limit=limit,
        include_only_user_ids=members_ids,
        exclude_user_ids=get_blocked_user_ids(db, user.user_id),
    )
    return {"entries": entries, "pagination": {"limit": limit, "offset": 0, "total": total}}


@router.get("/{group_id}/quests")
def group_quests(
    group_id: str,
    db: Session = Depends(get_db),
    user: UserContext = Depends(get_current_user),
) -> dict:
    """Active community challenges with live progress computed from the
    members' scored captures inside each quest window."""
    if get_group(db, group_id, user.user_id) is None:
        raise HTTPException(status_code=404, detail="Group not found")
    items = list_group_quests(
        db, group_id, group_member_ids(db, group_id), viewer_id=user.user_id)
    return {"items": items, "total": len(items)}


@router.get("/{group_id}/feed")
def group_feed(
    group_id: str,
    limit: int = Query(default=20, ge=1, le=50),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    user: UserContext = Depends(get_current_user),
) -> dict:
    """Recent public captures by this group's members."""
    if get_group(db, group_id, user.user_id) is None:
        raise HTTPException(status_code=404, detail="Group not found")
    members_ids = group_member_ids(db, group_id)
    return build_feed_page(db, user, limit, offset, restrict_user_ids=members_ids)
