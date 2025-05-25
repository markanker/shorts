from django.db import models
from django.contrib.auth.models import AbstractUser

import logging
logger = logging.getLogger('users')


class User(AbstractUser):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    pfp = models.ImageField(upload_to='pfps/', null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.pk:
            old_obj = User.objects.get(pk=self.pk)
            if self.pfp and old_obj.pfp != self.pfp:
                old_obj.pfp.delete(save=False)
        return super().save(*args, **kwargs)
