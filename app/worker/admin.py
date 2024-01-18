from django.contrib import admin
from django_celery_beat.models import IntervalSchedule, CrontabSchedule, SolarSchedule, ClockedSchedule, PeriodicTask
from django_celery_beat.admin import CrontabScheduleAdmin, PeriodicTaskAdmin
from django_celery_results.models import TaskResult, GroupResult
from django_celery_results.admin import TaskResultAdmin
from .models import DocType


admin.site.unregister(IntervalSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(SolarSchedule)
admin.site.unregister(ClockedSchedule)
admin.site.unregister(PeriodicTask)
admin.site.register(CrontabSchedule, CrontabScheduleAdmin)
admin.site.register(PeriodicTask, PeriodicTaskAdmin)

admin.site.unregister(TaskResult)
admin.site.unregister(GroupResult)

admin.site.register(TaskResult, TaskResultAdmin)

@admin.register(DocType)
class DocTypeAdmin(admin.ModelAdmin):
    list_display = ['slug', 'name']

