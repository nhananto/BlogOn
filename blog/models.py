from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=200)
    desc = models.TextField()
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    quote = models.CharField(max_length=200)