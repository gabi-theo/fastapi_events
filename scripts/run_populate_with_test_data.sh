cd ./app/
ls
python - <<EOF
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.db.database import Base, engine
from app.db.models import Bucket, Event

# Initialize tables
Base.metadata.create_all(bind=engine)

# Create a new session
db_session = Session(bind=engine)

# Create a bucket
new_bucket = Bucket(name="Sample Bucket")
db_session.add(new_bucket)
db_session.commit()

# Create an event associated with the bucket
new_event = Event(name="Sample Event", description="Event description", bucket=new_bucket)
db_session.add(new_event)
db_session.commit()

# Close the session
db_session.close()
EOF

echo "Data populated successfully."
