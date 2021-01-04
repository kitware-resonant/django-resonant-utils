from datetime import timedelta

from django.core.files.storage import Storage

try:
    from storages.backends.s3boto3 import S3Boto3Storage
except ImportError:
    # This should only be used for type interrogation, never instantiation
    S3Boto3Storage = type('FakeS3Boto3Storage', (), {})
try:
    from minio_storage.storage import MinioStorage
except ImportError:
    # This should only be used for type interrogation, never instantiation
    MinioStorage = type('FakeMinioStorage', (), {})


def expiring_url(storage: Storage, name: str, expiration: timedelta) -> str:
    """
    Return an expiring URL to a file name on a `Storage`.

    `S3Boto3Storage` and `MinioStorage` are specifically supported.
    """
    # Each storage backend uses a slightly different API for URL expiration
    if isinstance(storage, S3Boto3Storage):
        return storage.url(name, expire=int(expiration.total_seconds()))
    elif isinstance(storage, MinioStorage):
        return storage.url(name, max_age=expiration)
    else:
        # Unsupported Storage type
        return storage.url(name)
