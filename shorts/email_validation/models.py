from django.db import models
from users.models import User


class EmailVerificationModel(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='email_verify')
    code = models.TextField(max_length=30, unique=True)
    is_verified = models.BooleanField(default=False)
    hash_ip_address = models.TextField(max_length=15)
