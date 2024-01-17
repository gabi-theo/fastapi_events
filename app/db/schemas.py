from pydantic import BaseModel, UUID4, StringConstraints, ConfigDict
from typing import List
from typing_extensions import Annotated


class EventBase(BaseModel):
    name: str
    description: str


class EventCreate(EventBase):
    pass


class Event(EventBase):
    id: UUID4
    model_config = ConfigDict(from_attributes=True)


class BucketBase(BaseModel):
    name: str


class BucketCreate(BucketBase):
    name: Annotated[str, StringConstraints(pattern=r'^[a-zA-Z0-9_-]+$')]


class Bucket(BucketBase):
    id: UUID4
    events: List[Event] = []
    model_config = ConfigDict(from_attributes=True)
