from django.contrib import admin
from todolist.models import List, Task

admin.site.register(Task)
admin.site.register(List)
