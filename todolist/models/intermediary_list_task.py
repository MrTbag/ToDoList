from django.db import models
from todolist.models import List
from todolist.models import Task


class IntermediaryListTask(models.Model):
    List = models.ForeignKey(List, on_delete=models.CASCADE, default=None, null=True)
    Task = models.ForeignKey(Task, on_delete=models.CASCADE, default=None, null=True)
