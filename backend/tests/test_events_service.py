from datetime import date, timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.db.session import Base
from app.models.event import Event
from app.services.events import get_filtered_events, haversine_km


def setup_db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    session = sessionmaker(bind=engine)()
    today = date.today()
    session.add_all(
        [
            Event(
                name="Trail A",
                date=today + timedelta(days=2),
                distance_km=10,
                type="trail",
                location="Lugo",
                latitude=43.012,
                longitude=-7.555,
                source_url="https://example.com/a",
            ),
            Event(
                name="Road B",
                date=today + timedelta(days=5),
                distance_km=21,
                type="road",
                location="Vigo",
                latitude=42.232,
                longitude=-8.722,
                source_url="https://example.com/b",
            ),
        ]
    )
    session.commit()
    return session


def test_haversine_km_zero():
    assert haversine_km(0, 0, 0, 0) == 0


def test_get_filtered_events_by_type():
    db: Session = setup_db()
    events, total = get_filtered_events(db, event_type="trail")
    assert total == 1
    assert events[0].name == "Trail A"


def test_get_filtered_events_near():
    db: Session = setup_db()
    events, total = get_filtered_events(db, near=(43.012, -7.555), radius=5)
    assert total == 1
    assert events[0].location == "Lugo"
