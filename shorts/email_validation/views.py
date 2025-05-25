from .models import EmailVerificationModel
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from utils import get_hash_ip_address


@api_view(['GET'])
def verify_email_view(request, verif_code):
    if request.method == 'GET':
        hash_ip_address = get_hash_ip_address(request)

        try:
            user_to_verify = EmailVerificationModel.objects.get(hash_ip_address=hash_ip_address, is_verified=False)
        except EmailVerificationModel.DoesNotExist:
            return Response({}, status.HTTP_400_BAD_REQUEST)

        if user_to_verify.code == verif_code:
            user_to_verify.is_verified = True
            user_to_verify.save()
            return Response({}, status=status.HTTP_200_OK)
        # here return 400 and increase unsuccessful attempts counter
