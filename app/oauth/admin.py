from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as _UserAdmin
from django.utils.translation import gettext_lazy as _
from simple_history.admin import SimpleHistoryAdmin
from organization.models import UserToOrganization
from worker.models import WorkerDoc
from .models import User

admin.site.name = "Капитал кадри"
admin.site.site_header = "Капитал кадри"

class WorkerDocInline(admin.TabularInline):
    model = WorkerDoc
    extra = 0


class UserToOrganizationInline(admin.TabularInline):
    extra = 0
    model = UserToOrganization
    show_change_link = True
    verbose_name = "Организация"
    verbose_name_plural = "Организации"

@admin.register(User)
class UserAdmin(SimpleHistoryAdmin, _UserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "surname", "phone", "passport")}),
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
    inlines = [WorkerDocInline, UserToOrganizationInline]
    search_fields = User.autocomplete_search_fields()
    readonly_fields = ["date_joined", "last_login"]