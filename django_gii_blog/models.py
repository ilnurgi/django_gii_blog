from django.db import models

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=255)
    created = models.DateField(auto_created=True)
    updated = models.DateField(auto_now=True)
    text = models.TextField()
    short_text = models.TextField()