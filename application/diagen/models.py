from django.db import models


class Diagram(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    image_url = models.CharField(max_length=200)

    def __str__(self):
        return self.title
