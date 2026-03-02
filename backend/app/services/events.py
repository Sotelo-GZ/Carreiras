from __future__ import annotations

from datetime import date
from math import asin, cos, radians, sin, sqrt
from typing import Optional

from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.models.event import Event


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    earth_radius_km = 6371
    d_lat = radians(lat2 - lat1)
    d_lon = radians(lon2 - lon1)

    a = (
        sin(d_lat / 2) ** 2
        + cos(radians(lat1)) * cos(radians(lat2)) * sin(d_lon / 2) ** 2
    )
    c = 2 * asin(sqrt(a))
    return earth_radius_km * c


def get_filtered_events(
    db: Session,
    distance: Optional[float] = None,
    distance_min: Optional[float] = None,
    distance_max: Optional[float] = None,
    event_type: Optional[str] = None,
    from_date: Optional[date] = None,
    near: Optional[tuple[float, float]] = None,
    radius: Optional[float] = None,
    page: int = 1,
    page_size: int = 50,
):
    date_filter = from_date or date.today()
    conditions = [Event.date >= date_filter]

    if distance is not None:
        conditions.append(Event.distance_km == distance)
    if distance_min is not None:
        conditions.append(Event.distance_km >= distance_min)
    if distance_max is not None:
        conditions.append(Event.distance_km <= distance_max)
    if event_type:
        conditions.append(Event.type.ilike(event_type))

    query = select(Event).where(and_(*conditions)).order_by(Event.date.asc())
    events = list(db.scalars(query).all())

    if near and radius:
        lat, lng = near
        events = [
            event
            for event in events
            if haversine_km(lat, lng, event.latitude, event.longitude) <= radius
        ]

    total = len(events)
    start = (page - 1) * page_size
    end = start + page_size
    paginated = events[start:end]
    return paginated, total
