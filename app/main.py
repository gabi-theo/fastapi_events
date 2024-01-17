from fastapi import FastAPI

from app.db import models
from app.db.database import engine
from app.router import bucket, event


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(bucket.router, prefix="/v1/bucket", tags=["buckets"])
app.include_router(event.router, prefix="/v1", tags=["events"])
