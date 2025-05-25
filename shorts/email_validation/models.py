from django.db import models
from users.models import User
import datetime


class EmailVerificationModel(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='email_verify')
    code = models.TextField(max_length=30, unique=True)
    is_verified = models.BooleanField(default=False)
    hash_ip_address = models.TextField(max_length=15)
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    sent_mail_to_user_counter = models.PositiveSmallIntegerField(default=0)

    def is_expired(self):
        if datetime.datetime.now() - self.time_update >= datetime.timedelta(minutes=15):
            return self.verification_test_failed()
        return False

    def verification_test_failed(self):
        return self.user.delete()
