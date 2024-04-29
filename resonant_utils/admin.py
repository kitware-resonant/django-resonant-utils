from collections.abc import Callable
import itertools
from typing import TYPE_CHECKING, Generic, TypeVar

from django.contrib import admin
from django.contrib.admin.options import InlineModelAdmin
from django.db.models import Model
from django.http import HttpRequest

_ChildModelT = TypeVar("_ChildModelT", bound=Model)
_ParentModelT = TypeVar("_ParentModelT", bound=Model)

# https://mypy.readthedocs.io/en/latest/runtime_troubles.html#using-classes-that-are-generic-in-stubs-but-not-at-runtime
if TYPE_CHECKING:

    class _InlineMixin(InlineModelAdmin[_ChildModelT, _ParentModelT]):
        pass

    class _TabularInline(admin.TabularInline[_ChildModelT, _ParentModelT]):
        pass

else:

    class _InlineMixin(Generic[_ChildModelT, _ParentModelT]):
        pass

    class _TabularInline(Generic[_ChildModelT, _ParentModelT], admin.TabularInline):
        pass


class ReadonlyInlineMixin(_InlineMixin[_ChildModelT, _ParentModelT]):
    can_delete = False
    show_change_link = True
    view_on_site: bool | Callable[[_ChildModelT], str] = False
    extra = 0

    def get_readonly_fields(
        self, request: HttpRequest, obj: _ChildModelT | None = None
    ) -> list[str]:
        if self.fields is None:
            return []
        # Make all fields readonly
        # self.fields can contain nested sequences, but get_readonly_fields must return flattened
        return list(
            itertools.chain.from_iterable(
                [field_group] if isinstance(field_group, str) else field_group
                for field_group in self.fields
            )
        )

    def has_add_permission(self, request: HttpRequest, obj: _ParentModelT | None = None) -> bool:
        return False


class ReadonlyTabularInline(
    ReadonlyInlineMixin[_ChildModelT, _ParentModelT],
    _TabularInline[_ChildModelT, _ParentModelT],
):
    pass
