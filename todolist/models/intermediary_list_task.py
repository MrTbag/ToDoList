from django.db import models
from todolist.models import List
from todolist.models import Task

# TODO should class names be PascalCase?
class IntermediaryListTask(models.Model):
    List = models.ForeignKey(List, on_delete=models.CASCADE, default=None, null=True)
    Task = models.ForeignKey(Task, on_delete=models.CASCADE, default=None, null=True)
