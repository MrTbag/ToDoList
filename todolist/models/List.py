from django.db import models
from todolist.models import Task
from todolist.models import CustomUser

class List(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    pub_date = models.DateTimeField('date created', auto_now_add=True)
    tasks = models.ManyToManyField(Task, blank=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None, null=True)

    def __str__(self):
        return self.name