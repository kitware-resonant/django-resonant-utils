from django.contrib import admin


class ReadonlyInlineMixin:
    can_delete = False
    show_change_link = True
    view_on_site = False
    extra = 0

    def get_readonly_fields(self, request, obj=None):
        # Because BaseModelAdmin.get_fields calls BaseModelAdmin.get_readonly_fields, we cannot
        # get the list of fields from BaseModelAdmin.get_fields without infinite recursion.
        # So, basically reimplement BaseModelAdmin.get_fields here, and return the same fields,
        # thus making all fields readonly.
        if self.fields:
            return self.fields
        form = self._get_form_for_get_fields(request, obj)
        # Include any fields explicitly specified
        explicit_readonly_fields = self.readonly_fields
        return [*form.base_fields, *explicit_readonly_fields]

    def get_fields(self, request, obj=None):
        # get_readonly_fields now includes fields from form.base_fields, so get_fields should not
        # include it twice.
        self.get_readonly_fields(request, obj)

    def has_add_permission(self, request, obj=None):
        return False


class ReadonlyTabularInline(ReadonlyInlineMixin, admin.TabularInline):
    pass
