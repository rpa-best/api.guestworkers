from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from import_export.admin import ExportActionModelAdmin
from jet.admin import CompactInline
from rangefilter.filters import (
    DateRangeQuickSelectListFilterBuilder,
)
from .resources import OrganizationTabelResource
from .models import Organization, UserToOrganization, OrganizationDoc, OrganizationTabel


class UserToOrganizationInline(CompactInline):
    extra = 0
    model = UserToOrganization
    show_change_link = True
    autocomplete_fields = ("user",)


class OrganizationDocInline(admin.TabularInline):
    model = OrganizationDoc
    extra = 0


@admin.register(Organization)
class OrganizationAdmin(SimpleHistoryAdmin):
    list_display = ['name', 'inn']
    search_fields = ['name', 'inn']
    inlines = [UserToOrganizationInline, OrganizationDocInline]


@admin.register(OrganizationTabel)
class OrganizationTabelAdmin(ExportActionModelAdmin):
    list_display = ["org", "worker", "date", "value", "editable"]
    list_filter = ["org", "worker", ("date", DateRangeQuickSelectListFilterBuilder()),]
    resource_classes = [OrganizationTabelResource]
    
    def get_export_queryset(self, request):
        queryset = super().get_export_queryset(request)
        queryset.update(editable=False)
        return queryset
