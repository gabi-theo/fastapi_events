import uuid

from sqlalchemy import Column, ForeignKey, String, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from .database import Base


class Bucket(Base):
    __tablename__ = "buckets"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
        server_default=func.uuid_generate_v4(),
    )
    name = Column(String, index=True)

    events = relationship("Event", back_populates="bucket")


class Event(Base):
    __tablename__ = "events"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
        server_default=func.uuid_generate_v4(),
    )
    name = Column(String, index=True)
    description = Column(String, index=True)
    bucket_id = Column(UUID(as_uuid=True), ForeignKey("buckets.id"))

    bucket = relationship("Bucket", back_populates="events")
