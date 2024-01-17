import uuid

from fastapi import status
from fastapi.testclient import TestClient
from pytest import MonkeyPatch

from app.db import models
from app.services.bucket import BucketService


def test_create_bucket(test_client: TestClient, monkeypatch: MonkeyPatch):
    bucket_data = {"name": "test_bucket"}
    monkeypatch.setattr(
        BucketService,
        'get_bucket_by_name',
        lambda *args, **kwargs: None,
    )
    monkeypatch.setattr(
        BucketService,
        'create_bucket',
        lambda db, bucket: models.Bucket(id=str(uuid.uuid4()), **bucket.model_dump()),
    )

    response = test_client.post("/v1/bucket/", json=bucket_data)
    created_bucket = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert created_bucket["name"] == bucket_data["name"]


def test_create_bucket_invalid_name(test_client: TestClient, monkeypatch: MonkeyPatch):
    bucket_data = {"name": "test_bucket?"}
    monkeypatch.setattr(
        BucketService,
        'get_bucket_by_name',
        lambda *args, **kwargs: None,
    )
    monkeypatch.setattr(
        BucketService,
        'create_bucket',
        lambda db, bucket: models.Bucket(id=str(uuid.uuid4()), **bucket.model_dump()),
    )

    response = test_client.post("/v1/bucket/", json=bucket_data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_bucket_duplicate(test_client: TestClient, monkeypatch: MonkeyPatch):
    bucket_data = {"name": "test_bucket"}
    monkeypatch.setattr(
        BucketService,
        'get_bucket_by_name',
        lambda db, bucket_name: models.Bucket(id=str(uuid.uuid4()), name=bucket_name),
    )
    monkeypatch.setattr(
        BucketService,
        'create_bucket',
        lambda db, bucket: None,
    )

    response = test_client.post("/v1/bucket/", json=bucket_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Bucket with this name already exists" in response.text


def test_get_buckets(test_client: TestClient, monkeypatch: MonkeyPatch):
    mock_buckets = [
        models.Bucket(id=str(uuid.uuid4()), name=f"test_bucket_{i}") for i in range(5)
    ]
    monkeypatch.setattr(
        BucketService,
        'get_buckets_all',
        lambda db, skip, limit: mock_buckets,
    )

    response = test_client.get("/v1/bucket/")
    returned_buckets = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(returned_buckets) == len(mock_buckets)
    for returned_bucket, mock_bucket in zip(returned_buckets, mock_buckets):
        assert returned_bucket["id"] == str(mock_bucket.id)
        assert returned_bucket["name"] == mock_bucket.name


def test_get_buckets_empty(test_client: TestClient, monkeypatch: MonkeyPatch):
    monkeypatch.setattr(
        BucketService,
        'get_buckets_all',
        lambda db, skip, limit: [],
    )

    response = test_client.get("/v1/bucket/")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Buckets not found" in response.text
