from sqlalchemy.orm import Session
from typing import Optional

from app.db import models, schemas


class BucketService:
    @staticmethod
    def get_bucket_by_name(
        db: Session,
        bucket_name: str,
    ) -> Optional[models.Bucket]:
        return db.query(models.Bucket).filter(models.Bucket.name == bucket_name).first()

    @staticmethod
    def get_bucket_by_id(
        db: Session,
        bucket_id: str,
    ) -> Optional[models.Bucket]:
        return db.query(models.Bucket).filter(models.Bucket.id == bucket_id).first()

    @staticmethod
    def get_buckets_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> Optional[models.Bucket]:
        return db.query(models.Bucket).offset(skip).limit(limit).all()

    @staticmethod
    def create_bucket(
        db: Session,
        bucket: schemas.BucketCreate,
    ) -> Optional[models.Bucket]:
        db_bucket = models.Bucket(**bucket.model_dump())
        db.add(db_bucket)
        db.commit()
        db.refresh(db_bucket)
        return db_bucket
