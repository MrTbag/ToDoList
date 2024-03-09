from django.db import models
from todolist.models import CustomUser

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
