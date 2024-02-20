from django.contrib import admin
from todolist.models import List, Task


class TaskInLine(admin.TabularInline):
    model = Task
    extra = 3


class ListAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["name"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [TaskInLine]

    list_display = ["name", "pub_date"]

    list_filter = ["pub_date"]

    search_fields = ["name"]


admin.site.register(List, ListAdmin)
