from django.db import models
from django.contrib.auth.models import AbstractUser


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
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    pub_date = models.DateTimeField('date created')
    tasks = models.ManyToManyField(Task, null=True, blank=True)

    def __str__(self):
        return self.name


class Hash(models.Model):
    long_url = models.CharField(max_length=200)
    hashed = models.CharField(max_length=100)

    def __str__(self):
        return self.hashed


class CustomUser(AbstractUser):
    lists = models.ManyToManyField(List)
