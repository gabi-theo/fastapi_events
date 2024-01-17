from pydantic import UUID4
from sqlalchemy.orm import Session
from typing import Optional

from app.db import models, schemas


class EventService:
    @staticmethod
    def get_events_by_bucket(
        db: Session,
        bucket_id: UUID4,
        skip: int = 0,
        limit: int = 100
    ) -> Optional[models.Event]:
        return db.query(models.Event).offset(skip).limit(limit).filter(
            models.Event.bucket_id == bucket_id).all()

    @staticmethod
    def get_events_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> Optional[models.Event]:
        return db.query(models.Event).offset(skip).limit(limit).all()

    @staticmethod
    def get_event_details_for_bucket(
        db: Session,
        bucket_id: UUID4,
        event_id: UUID4,
    ) -> Optional[models.Event]:
        return db.query(models.Event).filter(
            models.Event.id == event_id,
            models.Event.bucket_id == bucket_id,
        )

    @staticmethod
    def create_event(
        db: Session,
        event: schemas.EventCreate,
        bucket_id: UUID4,
    ) -> Optional[models.Event]:
        db_event = models.Event(**event.model_dump(), bucket_id=bucket_id)
        db.add(db_event)
        db.commit()
        db.refresh(db_event)
        return db_event
