from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from import_export.admin import ExportActionModelAdmin
from unfold.admin import StackedInline, ModelAdmin
from rangefilter.filters import (
    DateRangeQuickSelectListFilterBuilder,
)
from .resources import OrganizationTabelResource
from .models import Organization, UserToOrganization, OrganizationDoc, OrganizationTabel, Document, DocumentType


class UserToOrganizationInline(StackedInline):
    extra = 0
    model = UserToOrganization
    show_change_link = True
    autocomplete_fields = ("user",)
    tab = True


class OrganizationDocInline(admin.TabularInline):
    model = OrganizationDoc
    extra = 0
    tab = True


@admin.register(Organization)
class OrganizationAdmin(SimpleHistoryAdmin, ModelAdmin):
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


@admin.register(DocumentType)
class DocumentType(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ["type", "date", "org"]
    list_filter = ["org", "type"]
    