from django.contrib import admin
from django_celery_beat.models import IntervalSchedule, SolarSchedule, ClockedSchedule
from django_celery_results.models import GroupResult
from .models import DocType


admin.site.unregister(IntervalSchedule)
admin.site.unregister(SolarSchedule)
admin.site.unregister(ClockedSchedule)

admin.site.unregister(GroupResult)

@admin.register(DocType)
class DocTypeAdmin(admin.ModelAdmin):
    list_display = ['slug', 'name']

