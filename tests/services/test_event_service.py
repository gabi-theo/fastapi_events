import uuid

from unittest.mock import MagicMock, patch

from app.services.event import EventService
from app.db import models


PATH = "app.services.event"


@patch(f"{PATH}.Session")
def test_get_events_by_bucket(
    patch_db: MagicMock,
):
    bucket_id = uuid.uuid4()
    patch_db.query().offset().limit().filter().all.return_value = ["event_1", "event_2"]

    result = EventService.get_events_by_bucket(db=patch_db, bucket_id=bucket_id, skip=0, limit=100)

    patch_db.query.assert_called_with(models.Event)
    patch_db.query().offset().limit().filter().all.assert_called_once()
    assert result == ["event_1", "event_2"]


@patch(f"{PATH}.Session")
def test_get_events_all(
    patch_db: MagicMock,
):
    db_session_mock = MagicMock()
    patch_db.query().offset().limit().all.return_value = ["event_1", "event_2"]

    result = EventService.get_events_all(db=patch_db, skip=0, limit=100)

    patch_db.query.assert_called_with(models.Event)
    patch_db.query().offset().limit().all.assert_called_once()
    assert result == ["event_1", "event_2"]


@patch(f"{PATH}.Session")
def test_get_event_details_for_bucket(
    patch_db: MagicMock,
):
    bucket_id = uuid.uuid4()
    event_id = uuid.uuid4()
    db_session_mock = MagicMock()
    patch_db.query().filter.return_value = db_session_mock

    result = EventService.get_event_details_for_bucket(
        db=patch_db, bucket_id=bucket_id, event_id=event_id)

    patch_db.query.assert_called_with(models.Event)
    assert result == db_session_mock


@patch("app.services.event.Session")
@patch("app.services.event.models.Event")
def test_create_event(
    event_patch: MagicMock,
    db_patch: MagicMock,
):
    db_session_mock = MagicMock()
    db_patch.return_value = db_session_mock
    db_session_add_mock = MagicMock()
    db_patch.add.return_value = db_session_add_mock
    event_mock = MagicMock()
    event_patch.return_value = event_mock

    event_create_mock = MagicMock()
    event_create_mock.model_dump.return_value = {"name": "test_event", "description": "Test description"}
    bucket_id_mock = uuid.uuid4()

    result = EventService.create_event(db=db_session_mock, event=event_create_mock, bucket_id=bucket_id_mock)

    db_session_mock.commit.assert_called_once()
    assert result == event_mock
