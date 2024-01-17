import uuid

from unittest.mock import MagicMock, patch

from app.services.bucket import BucketService
from app.db import models

PATH = 'app.services.bucket'


@patch(f"{PATH}.Session")
def test_get_bucket_by_name_exists(
    patch_db: MagicMock,
):
    mock_bucket_query = MagicMock(id=uuid.uuid4(), name="test_bucket")    
    patch_db.query().filter().first.return_value = mock_bucket_query

    result = BucketService.get_bucket_by_name(db=patch_db, bucket_name="test_bucket")

    assert result == mock_bucket_query


@patch(f"{PATH}.Session")
def test_get_bucket_by_name_not_exists(
    patch_db: MagicMock,
):
    bucket_name = "nonexistent_bucket"
    patch_db.query().filter().first.return_value = None

    result = BucketService.get_bucket_by_name(db=patch_db, bucket_name=bucket_name)

    assert result is None


@patch(f"{PATH}.Session")
def test_get_buckets_all(
    patch_db: MagicMock,
):
    bucket_instances = [models.Bucket(id=uuid.uuid4(), name=f"bucket_{i}") for i in range(1, 4)]
    patch_db.query().offset().limit().all.return_value = bucket_instances

    result = BucketService.get_buckets_all(db=patch_db, skip=0, limit=3)

    assert result == bucket_instances


def test_create_bucket():
    db_session_mock = MagicMock()
    db_session_mock.add = MagicMock()
    db_session_mock.commit = MagicMock()
    db_session_mock.refresh = MagicMock()
    bucket_model_mock = MagicMock()
    bucket_create_mock = MagicMock(name="test_bucket")
    bucket_create_mock.model_dump.return_value = {"name": "test_bucket"}

    with patch("app.services.bucket.models.Bucket", bucket_model_mock):
        BucketService.create_bucket(db=db_session_mock, bucket=bucket_create_mock)

    bucket_model_mock.assert_called_once_with(**bucket_create_mock.model_dump())
    db_session_mock.add.assert_called_once()
    db_session_mock.commit.assert_called_once()
