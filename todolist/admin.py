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

    list_display = ['name', 'pub_date', 'task_count']

    list_filter = ['pub_date']

    search_fields = ['name']

    def task_count(self, obj):
        from django.db.models import Count
        result = Task.objects.filter(list=obj).count()
        return result


admin.site.register(Task)
admin.site.register(List, ListAdmin)
