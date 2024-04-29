from datetime import timedelta

from django.core.files.storage import Storage

try:
    from storages.backends.s3 import S3Storage
except ImportError:
    # This should only be used for type interrogation, never instantiation
    S3Storage = type("FakeS3Storage", (), {})  # type: ignore[assignment,misc]
try:
    from minio_storage.storage import MinioStorage
except ImportError:
    # This should only be used for type interrogation, never instantiation
    MinioStorage = type("FakeMinioStorage", (), {})  # type: ignore[assignment,misc]


def expiring_url(storage: Storage, name: str, expiration: timedelta) -> str:
    """
    Return an expiring URL to a file name on a `Storage`.

    `S3Storage` and `MinioStorage` are specifically supported.
    """
    # Each storage backend uses a slightly different API for URL expiration
    if isinstance(storage, S3Storage):
        return storage.url(name, expire=int(expiration.total_seconds()))
    if isinstance(storage, MinioStorage):
        return storage.url(name, max_age=expiration)
    # Unsupported Storage type
    return storage.url(name)
