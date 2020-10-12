from contextlib import contextmanager
from pathlib import Path, PurePath
import shutil
import tempfile
from typing import Generator

from django.core.files import File
from django.db.models.fields.files import FieldFile


@contextmanager
def field_file_to_local_path(field_file: FieldFile) -> Generator[Path, None, None]:
    """
    Provide a filesystem path to the content of a FieldFile.

    Normally, a FieldFile is usable as a Python file-like object, as:
    `with model.field.open() as file_stream:`

    However, in some use cases, particularly when invoking third-party libraries,
    an actual filesystem path to the content is required. This context manager
    provides this as:
    `with field_file_to_local_path(model.field) as file_path:`

    When this context manager exists, the filesystem content and path will be
    garbage collected.
    """
    with field_file.open('rb'):
        file_obj: File = field_file.file

        if type(file_obj) is File:
            # When file_obj is an actual File, (typically backed by FileSystemStorage),
            # it is already at a stable path on disk.
            yield Path(file_obj.name)
        else:
            # When file_obj is actually a subclass of File, it only provides a Python
            # file-like object API. So, it must be copied to a stable path.
            field_file_basename = PurePath(field_file.name).name
            with tempfile.NamedTemporaryFile('wb', suffix=field_file_basename) as dest_stream:
                shutil.copyfileobj(file_obj, dest_stream)
                dest_stream.flush()

                yield Path(dest_stream.name)
