import itertools
from typing import TYPE_CHECKING, Callable, Optional, Sequence, TypeVar, Union

from django.contrib import admin
from django.contrib.admin.options import InlineModelAdmin
from django.db.models import Model
from django.http import HttpRequest

_ChildModelT = TypeVar('_ChildModelT', bound=Model)
_ParentModelT = TypeVar('_ParentModelT', bound=Model)

if TYPE_CHECKING:

    class InlineMixinBase(InlineModelAdmin[_ChildModelT, _ParentModelT]):
        pass

else:

    class InlineMixinBase:
        pass


class ReadonlyInlineMixin(InlineMixinBase[_ChildModelT, _ParentModelT]):
    can_delete = False
    show_change_link = True
    view_on_site: Union[bool, Callable[[_ChildModelT], str]] = False
    extra = 0

    def get_readonly_fields(
        self, request: HttpRequest, obj: Optional[_ChildModelT] = None
    ) -> Sequence[str]:
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

    def has_add_permission(self, request: HttpRequest, obj: Optional[_ParentModelT] = None) -> bool:
        return False


class ReadonlyTabularInline(
    ReadonlyInlineMixin[_ChildModelT, _ParentModelT],
    admin.TabularInline[_ChildModelT, _ParentModelT],
):
    pass
