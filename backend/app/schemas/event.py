from datetime import date

from pydantic import BaseModel


class EventRead(BaseModel):
    id: int
    name: str
    date: date
    distance_km: float
    type: str
    location: str
    latitude: float
    longitude: float
    source_url: str

    class Config:
        from_attributes = True
