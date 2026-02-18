from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Iterable, Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from dateutil import parser as date_parser

from app.core.config import settings
from app.services.geocoding import geocode_location

logger = logging.getLogger(__name__)


@dataclass
class ScrapedEvent:
    name: str
    date: datetime.date
    distance_km: float
    type: str
    location: str
    latitude: float
    longitude: float
    source_url: str


class ScraperStructureError(Exception):
    pass


def _extract_distance(text: str) -> Optional[float]:
    match = re.search(r"(\d+[\.,]?\d*)\s?(km|k)", text.lower())
    if not match:
        return None
    return float(match.group(1).replace(",", "."))


def _extract_type(text: str) -> str:
    lowered = text.lower()
    if "trail" in lowered:
        return "trail"
    if "asfalto" in lowered or "road" in lowered:
        return "road"
    if "montaña" in lowered or "montana" in lowered:
        return "mountain"
    return "running"


def _extract_date(text: str):
    return date_parser.parse(text, dayfirst=True, fuzzy=True).date()


def _event_cards(soup: BeautifulSoup) -> Iterable:
    selectors = [".event-item", ".events-item", "article", ".tribe-events-event", ".event"]
    for selector in selectors:
        cards = soup.select(selector)
        if len(cards) > 3:
            return cards
    raise ScraperStructureError("No event cards found with known selectors")


def scrape_events() -> list[ScrapedEvent]:
    response = requests.get(settings.scrape_source_url, timeout=settings.scrape_timeout_seconds)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    events: list[ScrapedEvent] = []
    cards = _event_cards(soup)

    for card in cards:
        try:
            title_el = card.select_one("h2, h3, .event-title, .tribe-event-title")
            meta_text = " ".join(card.stripped_strings)
            link_el = card.select_one("a[href]")

            if not title_el or not link_el:
                continue

            name = title_el.get_text(strip=True)
            date_value = _extract_date(meta_text)
            distance = _extract_distance(meta_text)
            location_match = re.search(r"(?:en|location|lugar)\s*[:\-]?\s*([A-Za-zÀ-ÿ\s\-']+)", meta_text, re.IGNORECASE)
            location = location_match.group(1).strip() if location_match else "Galicia"

            if distance is None:
                logger.info("Skipping event without distance: %s", name)
                continue

            coords = geocode_location(location)
            if not coords:
                logger.info("Skipping event without coordinates: %s", name)
                continue

            source_url = urljoin(settings.scrape_source_url, link_el["href"])

            events.append(
                ScrapedEvent(
                    name=name,
                    date=date_value,
                    distance_km=distance,
                    type=_extract_type(meta_text),
                    location=location,
                    latitude=coords[0],
                    longitude=coords[1],
                    source_url=source_url,
                )
            )
        except Exception as exc:  # parser hardening
            logger.warning("Could not parse card due to format change: %s", exc)

    if not events:
        logger.warning("Scraper completed with zero events.")

    return events
