from django.db import models
from links.models import Link


class Follower(models.Model):
    ip_address = models.GenericIPAddressField(max_length=15)
    country = models.TextField(max_length=250)
    city = models.TextField(max_length=250)


class LinkStats(models.Model):
    link = models.ForeignKey(to=Link, on_delete=models.CASCADE, related_name='stats')
    follower = models.ForeignKey(to=Follower, on_delete=models.CASCADE, related_name='stats', null=True, blank=True)
    is_owner = models.BooleanField(default=False)
    created_at = models.TimeField(auto_now_add=True)
    device = models.TextField(max_length=6, default='pc')
    browser_name = models.TextField(max_length=20)
    os_name = models.TextField(max_length=20, null=True, blank=True)
    os_version = models.TextField(max_length=10, null=True, blank=True)
