from .models import EmailVerificationModel
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from utils import get_hash_ip_address
from .utils import send_again
from exceptions import EmailVerificationError
from .permissions import IsAbleToSendAgain


@api_view(['GET'])
def verify_email_view(request, verif_code):
    hash_ip_address = get_hash_ip_address(request)

    try:
        user_to_verify = EmailVerificationModel.objects.get(hash_ip_address=hash_ip_address, is_verified=False)
    except EmailVerificationModel.DoesNotExist:
        return Response({}, status.HTTP_400_BAD_REQUEST)

    if user_to_verify.is_expired():
        return Response({}, status.HTTP_408_REQUEST_TIMEOUT)

    if user_to_verify.code == verif_code:
        user_to_verify.is_verified = True
        user_to_verify.save()
        return Response({}, status=status.HTTP_200_OK)

    return Response({'message': 'the provided code is incorrect'}, status.HTTP_400_BAD_REQUEST)


class SendAgainView(APIView):
    permission_classes = (IsAbleToSendAgain,)

    def get(self, request, *args, **kwargs):
        try:
            send_again(request)
        except EmailVerificationError as eve:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        return Response({}, status=status.HTTP_200_OK)
