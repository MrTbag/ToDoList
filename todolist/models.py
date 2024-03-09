from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

    def __str__(self):
        return self.username


class Task(models.Model):
    name = models.CharField(max_length=50)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None)
    done = models.BooleanField(default=False)
    importance = models.PositiveSmallIntegerField()
    date_added = models.DateTimeField('date added', auto_now_add=True)
    deadline = models.DateField('deadline')
    url = models.URLField(default=None, blank=True, null=True)
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
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None, null=True)

    def __str__(self):
        return self.name


class IntermediaryListTask(models.Model):
    List = models.ForeignKey(List, on_delete=models.CASCADE, default=None, null=True)
    Task = models.ForeignKey(Task, on_delete=models.CASCADE, default=None, null=True)
