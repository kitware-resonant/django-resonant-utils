from collections.abc import Sequence
import json
from typing import Any, TypeVar

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Manager, Model, QuerySet
from django.utils.translation import gettext_lazy as _

_T = TypeVar("_T", bound=Model, covariant=True)


class JSONObjectField(models.JSONField):
    """
    A field for storing JSON Objects.

    Other JSON types are not allowed at the top level.
    """

    @staticmethod
    def _validate_is_object(val: Any) -> None:
        """Validate that the value is a JSON Object (dict) at the top level."""
        if not isinstance(val, dict):
            raise ValidationError(_("Must be a JSON Object."))

    empty_values: list[Any] = [{}]

    # At this point in the class definition lifecycle,
    # staticmethods aren't resolvable directly, so use "__func__"
    # https://stackoverflow.com/questions/41921255/staticmethod-object-is-not-callable
    # Additionally, MyPy has a bug here: https://github.com/python/mypy/issues/3482
    default_validators = [_validate_is_object.__func__]  # type: ignore[attr-defined]

    def __init__(
        self,
        verbose_name: str | None = None,
        name: str | None = None,
        encoder: type[json.JSONEncoder] | None = None,
        decoder: type[json.JSONDecoder] | None = None,
        **kwargs: Any,
    ) -> None:
        kwargs["default"] = dict
        kwargs["blank"] = True
        super().__init__(
            verbose_name=verbose_name, name=name, encoder=encoder, decoder=decoder, **kwargs
        )

    def deconstruct(self) -> tuple[str, str, Sequence[Any], dict[str, Any]]:
        name, path, args, kwargs = super().deconstruct()
        del kwargs["default"]
        del kwargs["blank"]
        return name, path, args, kwargs


class SelectRelatedManager(Manager[_T]):
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
        self.related_fields: list[str] = list(related_fields)
        super().__init__()

    def get_queryset(self) -> QuerySet[_T]:
        return super().get_queryset().select_related(*self.related_fields)


class DeferredFieldsManager(Manager[_T]):
    """A Manager which defers loading specified fields within fetched Models."""

    def __init__(self, *deferred_fields: str) -> None:
        self.deferred_fields = deferred_fields
        super().__init__()

    def get_queryset(self) -> QuerySet[_T]:
        return super().get_queryset().defer(*self.deferred_fields)
