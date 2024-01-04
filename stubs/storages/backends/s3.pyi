from typing import Any, Optional

from django.utils.deconstruct import deconstructible
from storages.base import BaseStorage
from storages.compress import CompressStorageMixin

@deconstructible
class S3Storage(CompressStorageMixin, BaseStorage):
    def url(  # type: ignore[override]
        self,
        name: str,
        parameters: Optional[dict[str, Any]] = None,
        expire: Optional[int] = None,
        http_method: Optional[str] = None,
    ) -> str: ...
