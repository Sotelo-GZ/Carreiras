from __future__ import annotations

from typing import Optional, Tuple

import requests

from app.core.config import settings


class GeocodingError(Exception):
    pass


def geocode_location(location: str) -> Optional[Tuple[float, float]]:
    params = {
        "q": f"{location}, Galicia, Spain",
        "format": "json",
        "limit": 1,
    }
    headers = {"User-Agent": settings.geocode_user_agent}

    try:
        response = requests.get(
            settings.geocode_url,
            params=params,
            headers=headers,
            timeout=settings.scrape_timeout_seconds,
        )
        response.raise_for_status()
        payload = response.json()
    except requests.RequestException as exc:
        raise GeocodingError(f"Geocoding request failed for '{location}'") from exc

    if not payload:
        return None

    return float(payload[0]["lat"]), float(payload[0]["lon"])
