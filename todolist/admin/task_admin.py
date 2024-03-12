from django.contrib import admin
from todolist.models import Task


class TaskAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
        (None, {'fields': ['importance']}),
    ]

    list_display = ['name', 'date_added', 'creator', 'done']

    list_filter = ['date_added', 'deadline']


admin.site.register(Task, TaskAdmin)
