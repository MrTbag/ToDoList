from django.db import models
from todolist.models import Task
from todolist.models import CustomUser


class TodoList(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    pub_date = models.DateTimeField('date created', auto_now_add=True)
    tasks = models.ManyToManyField(Task, blank=True)
    # TODO how to add new mandatory data to database without dropping the database or setting defaults for the new
    #  fields
    # TODO how to handle python scripts in migration files
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None, null=True)

    def __str__(self):
        return self.name
