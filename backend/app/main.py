from __future__ import annotations

import logging

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI

from app.api.events import router as events_router
from app.db.session import Base, SessionLocal, engine
from app.services.ingestion import run_scrape_job

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Carreiras API")
app.include_router(events_router)

scheduler = BackgroundScheduler(timezone="Europe/Madrid")


def scheduled_scrape():
    db = SessionLocal()
    try:
        run_scrape_job(db)
    except Exception as exc:
        logger.exception("Scheduled scrape failed: %s", exc)
    finally:
        db.close()


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    scheduled_scrape()
    scheduler.add_job(scheduled_scrape, "interval", days=1, id="daily_scrape", replace_existing=True)
    scheduler.start()


@app.on_event("shutdown")
def shutdown():
    if scheduler.running:
        scheduler.shutdown()


@app.get("/health")
def health_check():
    return {"status": "ok"}
