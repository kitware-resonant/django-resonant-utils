import datetime
from typing import Optional

from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible

@deconstructible
class MinioStorage(Storage):
    def url(self, name: str, *, max_age: Optional[datetime.timedelta] = None) -> str: ...  # type: ignore[override]
