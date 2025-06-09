from .models import EmailVerificationModel
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from utils import get_hash_ip_address
from .utils import send_again
from exceptions import EmailVerificationError
from .permissions import IsAbleToSendAgain

import logging
logger = logging.getLogger('email_validation')


@api_view(['GET'])
def verify_email_view(request, verif_code):
    hash_ip_address = get_hash_ip_address(request)

    try:
        user_to_verify = EmailVerificationModel.objects.get(
            code=verif_code,
            hash_ip_address=hash_ip_address,
            is_verified=False,
        )
    except EmailVerificationModel.DoesNotExist:
        return Response({'message': 'there is no such code you provided'}, status.HTTP_400_BAD_REQUEST)

    if user_to_verify.is_expired():
        return Response({'message': 'your verification code is expired, so we are '
                                    'supposed to delete your account'}, status.HTTP_408_REQUEST_TIMEOUT)

    if user_to_verify.code == verif_code:
        user_to_verify.is_verified = True
        user_to_verify.save()
        return Response({'message': 'your email was successfully verified'}, status=status.HTTP_200_OK)

    return Response({'message': 'the provided code is incorrect'}, status.HTTP_400_BAD_REQUEST)


class SendAgainView(APIView):
    permission_classes = (IsAbleToSendAgain,)

    def get(self, request, *args, **kwargs):
        try:
            send_again(request)
        except EmailVerificationError as eve:
            return Response({'error': str(eve)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'the code was sent again on your email'}, status=status.HTTP_200_OK)
