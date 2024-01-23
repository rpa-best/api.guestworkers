from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from jet.admin import CompactInline
from .models import Organization, UserToOrganization


class UserToOrganizationInline(CompactInline):
    extra = 0
    model = UserToOrganization
    show_change_link = True
    raw_id_fields = ("user",)
    non_editable_fields = ['user']

    def get_fields(self, request, obj=None):
        defaults = super().get_fields(request, obj=obj)
        if obj: # if we are updating an object
            defaults = tuple(f for f in defaults if f not in self.non_editable_fields)
        return defaults


@admin.register(Organization)
class OrganizationAdmin(SimpleHistoryAdmin):
    list_display = ['name', 'inn']
    search_fields = ['name', 'inn']
    inlines = [UserToOrganizationInline]
