from django.db import models


class List(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    pub_date = models.DateTimeField('date created')

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=50)
    done = models.BooleanField(default=False)
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    importance = models.IntegerField()
    date_added = models.DateTimeField('date added')
    deadline = models.DateField('deadline')

    class Meta:
        ordering = ('importance', 'date_added', )

    def __str__(self):
        return self.name


