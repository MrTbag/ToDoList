from django.db import models
from todolist.models import TodoList
from todolist.models import Task


class IntermediaryTodoListTask(models.Model):
    List = models.ForeignKey(TodoList, on_delete=models.CASCADE, default=None, null=True)
    Task = models.ForeignKey(Task, on_delete=models.CASCADE, default=None, null=True)
