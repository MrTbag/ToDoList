from django.db import models


class UrlDict(models.Model):
    key = models.CharField(max_length=200)
    original_url = models.CharField(max_length=500)

    def __str__(self):
        return self.key
