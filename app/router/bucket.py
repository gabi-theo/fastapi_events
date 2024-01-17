import logging

from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from app.db import models, schemas
from app.db.database import engine, get_db
from app.services.bucket import BucketService

models.Base.metadata.create_all(bind=engine)

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/", response_model=schemas.Bucket)
async def create_bucket(bucket: schemas.BucketCreate, db: Session = Depends(get_db)):
    logger.info("Creating buckets")
    db_bucket = BucketService.get_bucket_by_name(db, bucket_name=bucket.name)
    if db_bucket:
        logger.error("Bucket with this name already exists")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bucket with this name already exists")
    return BucketService.create_bucket(db=db, bucket=bucket)


@router.get("/", response_model=list[schemas.Bucket])
async def get_buckets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logger.info("Getting buckets")
    buckets = BucketService.get_buckets_all(db=db, skip=skip, limit=limit)
    if not buckets:
        logger.error("Buckets not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Buckets not found")
    return buckets
