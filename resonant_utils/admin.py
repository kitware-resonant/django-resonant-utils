from __future__ import annotations

import itertools
from typing import TYPE_CHECKING

from django.contrib import admin
from django.db.models import Model

# https://mypy.readthedocs.io/en/latest/runtime_troubles.html#using-classes-that-are-generic-in-stubs-but-not-at-runtime
if TYPE_CHECKING:
    from collections.abc import Callable

    from django.contrib.admin.options import InlineModelAdmin
    from django.http import HttpRequest

    class _InlineMixin[ChildModelT: Model, ParentModelT: Model](
        InlineModelAdmin[ChildModelT, ParentModelT]
    ):
        pass

    class _TabularInline[ChildModelT: Model, ParentModelT: Model](
        admin.TabularInline[ChildModelT, ParentModelT]
    ):
        pass

else:

    class _InlineMixin[ChildModelT: Model, ParentModelT: Model]:
        pass

    class _TabularInline[ChildModelT: Model, ParentModelT: Model](admin.TabularInline):
        pass


class ReadonlyInlineMixin[ChildModelT: Model, ParentModelT: Model](
    _InlineMixin[ChildModelT, ParentModelT]
):
    can_delete = False
    show_change_link = True
    view_on_site: bool | Callable[[ChildModelT], str] = False
    extra = 0

    def get_readonly_fields(
        self, request: HttpRequest, obj: ChildModelT | None = None
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

    def has_add_permission(self, request: HttpRequest, obj: ParentModelT | None = None) -> bool:
        return False


class ReadonlyTabularInline[ChildModelT: Model, ParentModelT: Model](
    ReadonlyInlineMixin[ChildModelT, ParentModelT],
    _TabularInline[ChildModelT, ParentModelT],
):
    pass
