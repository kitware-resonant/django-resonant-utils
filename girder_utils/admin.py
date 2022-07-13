from typing import Callable, Union

from django.contrib import admin


class ReadonlyInlineMixin:
    can_delete = False
    show_change_link = True
    # Add this type definition to make the type checker happy
    view_on_site: Union[bool, Callable] = False
    extra = 0

    def get_readonly_fields(self, request, obj=None):
        if self.fields is None:
            return []
        # Make all fields readonly
        return self.fields

    def has_add_permission(self, request, obj=None):
        return False


class ReadonlyTabularInline(ReadonlyInlineMixin, admin.TabularInline):
    pass
