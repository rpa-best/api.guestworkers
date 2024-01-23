from typing import Any, List, Tuple
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as _UserAdmin
from django.http.request import HttpRequest
from django.utils.translation import gettext_lazy as _
from simple_history.admin import SimpleHistoryAdmin
from worker.models import WorkerDoc
from .models import User

admin.site.name = "Капитал кадри"
admin.site.site_header = "Капитал кадри"

class WorkerDocInline(admin.TabularInline):
    model = WorkerDoc
    extra = 0
    non_editable_fields = ['type']

    def get_readonly_fields(self, request, obj=None):
        defaults = super().get_readonly_fields(request, obj)
        if obj: # if we are updating an object
            defaults = tuple(f for f in defaults if f in self.non_editable_fields)
        return defaults


@admin.register(User)
class UserAdmin(SimpleHistoryAdmin, _UserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "surname", "phone")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    list_display = ("email", "first_name", "last_name", "surname", "is_staff")
    ordering = ("email",)
    inlines = [WorkerDocInline]
    search_fields = ["email", "first_name", "last_name", "surname"]