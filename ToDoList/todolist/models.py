from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    name = models.CharField(max_length=50)
    done = models.BooleanField(default=False)
    importance = models.IntegerField()
    date_added = models.DateTimeField('date added')
    deadline = models.DateField('deadline')

    class Meta:
        ordering = ('importance', 'date_added',)

    def __str__(self):
        return self.name


class List(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField(blank=True)
    pub_date = models.DateTimeField('date created', null=True, blank=True)
    tasks = models.ManyToManyField(Task, null=True, blank=True)

    def __str__(self):
        return self.name

