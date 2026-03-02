from __future__ import annotations

from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.event import EventRead
from app.services.events import get_filtered_events

router = APIRouter(prefix="/events", tags=["events"])


@router.get("", response_model=list[EventRead])
def list_events(
    distance: Optional[float] = None,
    distance_min: Optional[float] = Query(default=None, alias="distanceMin"),
    distance_max: Optional[float] = Query(default=None, alias="distanceMax"),
    type: Optional[str] = None,
    from_date: Optional[date] = Query(default=None, alias="from"),
    near: Optional[str] = None,
    radius: Optional[float] = None,
    page: int = 1,
    page_size: int = Query(default=50, le=100),
    db: Session = Depends(get_db),
):
    near_tuple = None
    if near:
        lat, lng = near.split(",")
        near_tuple = (float(lat), float(lng))

    events, _ = get_filtered_events(
        db,
        distance=distance,
        distance_min=distance_min,
        distance_max=distance_max,
        event_type=type,
        from_date=from_date,
        near=near_tuple,
        radius=radius,
        page=page,
        page_size=page_size,
    )
    return events
