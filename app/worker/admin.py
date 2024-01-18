from django.contrib import admin
from .models import DocType


@admin.register(DocType)
class DocTypeAdmin(admin.ModelAdmin):
    list_display = ['slug', 'name']

