from rest_framework.permissions import BasePermission
from email_validation.models import EmailVerificationModel
from utils import get_hash_ip_address


class IsValidEmail(BasePermission):
    def has_permission(self, request, view):
        try:
            user_email_verified = EmailVerificationModel.objects.get(
                hash_ip_address=get_hash_ip_address(request)
            )
        except EmailVerificationModel.DoesNotExist:
            return False

        return user_email_verified.is_verified
