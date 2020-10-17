from django.contrib import admin


class ReadonlyTabularInline(admin.TabularInline):
    can_delete = False
    show_change_link = True
    view_on_site = False
    extra = 0

    def get_readonly_fields(self, request, obj=None):
        return self.fields

    def has_add_permission(self, request, obj=None):
        return False
