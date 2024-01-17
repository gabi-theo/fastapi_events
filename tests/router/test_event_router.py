import uuid

from fastapi import status
from fastapi.testclient import TestClient
from pytest import MonkeyPatch

from app.db import models
from app.services.event import EventService
from app.services.bucket import BucketService


def test_get_events(test_client: TestClient, monkeypatch: MonkeyPatch):
    mock_events = [
        models.Event(id=str(uuid.uuid4()), name=f"test_event_{i}", description=f"Description {i}")
        for i in range(5)
    ]
    monkeypatch.setattr(
        EventService,
        'get_events_all',
        lambda db, skip, limit: mock_events,
    )

    response = test_client.get("/v1/events/")
    returned_events = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(returned_events) == len(mock_events)
    for returned_event, mock_event in zip(returned_events, mock_events):
        assert returned_event["id"] == str(mock_event.id)
        assert returned_event["name"] == mock_event.name
        assert returned_event["description"] == mock_event.description


def test_get_events_empty(test_client: TestClient, monkeypatch: MonkeyPatch):
    monkeypatch.setattr(
        EventService,
        'get_events_all',
        lambda db, skip, limit: [],
    )

    response = test_client.get("/v1/events/")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Events not found" in response.text


def test_create_event_for_bucket(test_client: TestClient, monkeypatch: MonkeyPatch):
    mock_bucket_id = str(uuid.uuid4())
    mock_bucket = models.Bucket(id=mock_bucket_id, name="test_bucket")
    monkeypatch.setattr(
        BucketService,
        'get_bucket_by_id',
        lambda db, bucket_id: mock_bucket,
    )
    monkeypatch.setattr(
        EventService,
        'create_event',
        lambda db, event, bucket_id: models.Event(id=str(uuid.uuid4()), **event.model_dump(), bucket_id=bucket_id),
    )

    event_data = {"name": "test_event", "description": "Test event description"}

    response = test_client.post(f"/v1/{mock_bucket_id}/", json=event_data)
    created_event = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert created_event["name"] == event_data["name"]
    assert created_event["description"] == event_data["description"]


def test_create_event_for_bucket_invalid_bucket(test_client: TestClient, monkeypatch: MonkeyPatch):
    mock_bucket_id = str(uuid.uuid4())
    mock_event_id = str(uuid.uuid4())
    monkeypatch.setattr(
        BucketService,
        'get_bucket_by_id',
        lambda db, bucket_id: None,
    )

    event_data = {"name": "test_event", "description": "Test event description"}

    response = test_client.post(f"/v1/{mock_bucket_id}/{mock_event_id}/", json=event_data)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Bucket not found" in response.text


def test_create_event_for_bucket_invalid_bucket(test_client: TestClient, monkeypatch: MonkeyPatch):
    mock_bucket_id = str(uuid.uuid4())
    monkeypatch.setattr(
        BucketService,
        'get_bucket_by_id',
        lambda db, bucket_id: None,
    )

    event_data = {"name": "test_event", "description": "Test event description"}

    response = test_client.post(f"/v1/{mock_bucket_id}/", json=event_data)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Bucket not found" in response.text


def test_get_events_for_bucket(test_client: TestClient, monkeypatch: MonkeyPatch):
    mock_bucket_id = str(uuid.uuid4())
    mock_events = [
        {"id": str(uuid.uuid4()), "name": "event1", "description": "Event 1 description"},
        {"id": str(uuid.uuid4()), "name": "event2", "description": "Event 2 description"},
    ]
    monkeypatch.setattr(
        EventService,
        'get_events_by_bucket',
        lambda db, bucket_id, skip, limit: mock_events,
    )

    response = test_client.get(f"/v1/{mock_bucket_id}/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == mock_events


def test_get_event_details_for_bucket(test_client: TestClient, monkeypatch: MonkeyPatch):
    mock_bucket_id = str(uuid.uuid4())
    mock_event_id = str(uuid.uuid4())
    mock_event = {"id": mock_event_id, "name": "test_event", "description": "Test event description"}
    monkeypatch.setattr(
        EventService,
        'get_event_details_for_bucket',
        lambda db, bucket_id, event_id: [mock_event],
    )

    response = test_client.get(f"/v1/{mock_bucket_id}/{mock_event_id}/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [mock_event]
