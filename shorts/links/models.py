from django.db import models
from users.models import User


class Link(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='links', null=True, blank=True)
    session_key = models.CharField(max_length=32, null=True, blank=True)
    source_link = models.TextField(max_length=250)
    short_link = models.TextField(max_length=15, unique=True)
