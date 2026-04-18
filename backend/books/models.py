from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    rating = models.FloatField()
    description = models.TextField()
    url = models.URLField()

    def __str__(self):
        return self.title
