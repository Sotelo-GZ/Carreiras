from __future__ import annotations

import logging

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.event import Event
from app.scraper.carreiras_scraper import scrape_events

logger = logging.getLogger(__name__)


def run_scrape_job(db: Session) -> int:
    scraped_events = scrape_events()
    upserted = 0

    for item in scraped_events:
        existing = db.scalar(
            select(Event).where(
                Event.name == item.name,
                Event.date == item.date,
                Event.distance_km == item.distance_km,
            )
        )

        if existing:
            existing.type = item.type
            existing.location = item.location
            existing.latitude = item.latitude
            existing.longitude = item.longitude
            existing.source_url = item.source_url
        else:
            db.add(
                Event(
                    name=item.name,
                    date=item.date,
                    distance_km=item.distance_km,
                    type=item.type,
                    location=item.location,
                    latitude=item.latitude,
                    longitude=item.longitude,
                    source_url=item.source_url,
                )
            )
        upserted += 1

    db.commit()
    logger.info("Scrape job finished. Upserted=%s", upserted)
    return upserted
