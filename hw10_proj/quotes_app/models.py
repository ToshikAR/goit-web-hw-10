from datetime import datetime
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Author(models.Model):
    fullname = models.CharField(max_length=100, null=False, unique=True)
    born_date = models.DateField()
    born_location = models.CharField(max_length=150)
    description = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.fullname

    class Meta:
        ordering = ["fullname"]


class Tag(models.Model):
    name = models.CharField(max_length=50, null=False)

    def __str__(self):
        return f"{self.name}"


class Quote(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, default=None, null=True)
    tags = models.ManyToManyField(Tag)
    quote = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def get_tags(self):
        return self.tags.split(",")
