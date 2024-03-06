from django.contrib import admin
from todolist.models import List, Task


class TaskInline(admin.TabularInline):
    model = List.tasks.through
    extra = 2


class ListAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
        ('Description', {'fields': ['description'], 'classes': ['collapse']}),
    ]
    inlines = [TaskInline]

    list_display = ['name', 'pub_date', 'task_count', 'owner']

    list_filter = ['pub_date']

    search_fields = ['name', ]

    @staticmethod
    def task_count(obj):
        result = Task.objects.filter(list=obj).count()
        return result


class TaskAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
        (None, {'fields': ['importance']}),
    ]

    list_display = ['name', 'date_added', 'creator', 'done']

    list_filter = ['date_added', 'deadline']


admin.site.register(Task, TaskAdmin)
admin.site.register(List, ListAdmin)
