from django.db import models
from django.contrib.auth.models import AbstractUser


class Task(models.Model):
    name = models.CharField(max_length=50)
    done = models.BooleanField(default=False)
    importance = models.IntegerField()
    date_added = models.DateTimeField('date added', auto_now_add=True)
    deadline = models.DateField('deadline')
    file = models.FileField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    class Meta:
        ordering = ('importance', 'date_added',)

    def __str__(self):
        return self.name


class List(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    pub_date = models.DateTimeField('date created', auto_now_add=True)
    tasks = models.ManyToManyField(Task, blank=True)

    def __str__(self):
        return self.name


class Hash(models.Model):
    long_url = models.CharField(max_length=200)
    hashed = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.hashed


class CustomUser(AbstractUser):
    lists = models.ManyToManyField(List)
