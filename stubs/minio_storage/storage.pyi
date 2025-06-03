import datetime

from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible

@deconstructible
class MinioStorage(Storage):
    def url(self, name: str, *, max_age: datetime.timedelta | None = None) -> str: ...  # type: ignore[override]
