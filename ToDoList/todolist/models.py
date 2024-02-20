from django.db import models


class List(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=50)
    done = models.BooleanField(default=False)
    list = models.ForeignKey(List, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    
