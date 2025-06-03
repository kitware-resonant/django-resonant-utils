from typing import Any

from django.utils.deconstruct import deconstructible
from storages.base import BaseStorage
from storages.compress import CompressStorageMixin

@deconstructible
class S3Storage(CompressStorageMixin, BaseStorage):
    def url(  # type: ignore[override]
        self,
        name: str,
        parameters: dict[str, Any] | None = None,
        expire: int | None = None,
        http_method: str | None = None,
    ) -> str: ...
