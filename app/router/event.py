import logging

from fastapi import Depends, APIRouter, HTTPException, status
from pydantic import UUID4
from sqlalchemy.orm import Session

from app.db import models, schemas
from app.db.database import engine, get_db
from app.services.bucket import BucketService
from app.services.event import EventService


models.Base.metadata.create_all(bind=engine)

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/events/", response_model=list[schemas.Event])
async def get_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logger.info("Getting events")
    events = EventService.get_events_all(db=db, skip=skip, limit=limit)
    if not events:
        logger.error("Events not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Events not found")
    return events


@router.post("/{bucket_id}/", response_model=schemas.Event)
async def create_event_for_bucket(
    bucket_id: UUID4,
    event: schemas.EventCreate,
    db: Session = Depends(get_db)
):
    logger.info("Creating event")
    db_bucket = BucketService.get_bucket_by_id(db, bucket_id=bucket_id)
    if not db_bucket:
        logger.error("Bucket not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bucket not found")    
    return EventService.create_event(db=db, event=event, bucket_id=bucket_id)


@router.get("/{bucket_id}/", response_model=list[schemas.Event])
async def get_events_for_bucket(
    bucket_id: UUID4, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    logger.info(f"Getting events for bucket {bucket_id}")
    events = EventService.get_events_by_bucket(db=db, bucket_id=bucket_id, skip=skip, limit=limit)
    if not events:
        logger.error(f"events not found for bucket with id: {bucket_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Events not found")
    return events

@router.get("/{bucket_id}/{event_id}/", response_model=list[schemas.Event])
async def get_events(
    bucket_id: UUID4,
    event_id: UUID4,
    db: Session = Depends(get_db)
):
    logger.info(f"Getting event {event_id} for bucket {bucket_id}")
    events = EventService.get_event_details_for_bucket(
        db=db,
        bucket_id=bucket_id,
        event_id=event_id,
    )
    if not events:
        logger.error(f"No event with id {event_id} for bucket {bucket_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Events not found")
    return events
