from django.contrib import admin
from todolist.models import TodoList, Task


class TaskInline(admin.TabularInline):
    model = TodoList.tasks.through
    extra = 2


class TodoListAdmin(admin.ModelAdmin):
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


admin.register(TodoList, TodoListAdmin)
