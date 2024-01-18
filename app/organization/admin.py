from django.contrib import admin


from .models import Organization, UserToOrganization


class UserToOrganizationInline(admin.TabularInline):
    extra = 0
    model = UserToOrganization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'inn']
    search_fields = ['name', 'inn']
    inlines = [UserToOrganizationInline]