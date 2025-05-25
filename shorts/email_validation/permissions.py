from rest_framework.permissions import BasePermission
from email_validation.models import EmailVerificationModel
from utils import get_hash_ip_address
import datetime


class IsValidEmail(BasePermission):
    def has_permission(self, request, view):
        try:
            email_code = EmailVerificationModel.objects.get(
                hash_ip_address=get_hash_ip_address(request)
            )
        except EmailVerificationModel.DoesNotExist:
            return False

        return email_code.is_verified


class IsAbleToSendAgain(BasePermission):
    def has_permission(self, request, view):
        try:
            email_code = EmailVerificationModel.objects.get(
                hash_ip_address=get_hash_ip_address(request)
            )
        except EmailVerificationModel.DoesNotExist:
            return False

        if datetime.datetime.now() - email_code.time_update < datetime.timedelta(minutes=5):
            return False

        if email_code.sent_mail_to_user_counter < 3:
            email_code.verification_test_failed()
            return False

        if email_code.is_expired():
            return False

        return True
