from django.db import models

class FileInfo(models.Model):

    name = models.CharField(max_length=100)
    file = models.FileField()

    def __str__(self):
        return self.name
