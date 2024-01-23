from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from jet.admin import CompactInline
from .models import Organization, UserToOrganization


class UserToOrganizationInline(CompactInline):
    extra = 0
    model = UserToOrganization
    show_change_link = True
    raw_id_fields = ("user",)


@admin.register(Organization)
class OrganizationAdmin(SimpleHistoryAdmin):
    list_display = ['name', 'inn']
    search_fields = ['name', 'inn']
    inlines = [UserToOrganizationInline]
