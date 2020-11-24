from typing import Any, List

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Manager, QuerySet


def _validate_metadata(val) -> None:
    if not isinstance(val, dict):
        raise ValidationError('Must be a JSON Object.')


class JSONObjectField(models.JSONField):  # type: ignore
    """A field for storing JSON Objects."""

    empty_values: List[Any] = [{}]

    def __init__(self, *args, **kwargs):
        kwargs['default'] = dict
        kwargs['blank'] = True
        super().__init__(*args, **kwargs)
        self.validators.append(_validate_metadata)


class SelectRelatedManager(Manager):
    """
    A Manager which always follows specified foreign-key relationships.

    For Models which very frequently need to follow foreign-key relationships
    (e.g. to generate their own __str__), it may be best to make this the
    "_default_manager", so many automatically generated queries are more
    efficient. To do so, define a custom "objects" as the first
    Manager in the Model:
        objects = SelectRelatedManager('foreign_thing')

    Passing no arguments makes this follow all the Model's non-null
    foreign-key relationships.
    """

    def __init__(self, *related_fields: str) -> None:
        self.related_fields: List[str] = list(related_fields)
        super().__init__()

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().select_related(*self.related_fields)


class DeferredFieldsManager(Manager):
    """A Manager which defers loading specified fields within fetched Models."""

    def __init__(self, *deferred_fields):
        self.deferred_fields = deferred_fields
        super().__init__()

    def get_queryset(self):
        return super().get_queryset().defer(*self.deferred_fields)
