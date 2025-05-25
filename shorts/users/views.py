from django.contrib import auth
from django.db import IntegrityError
from rest_framework import views, status, viewsets, mixins
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from links.models import Link
from users.models import User
from .serializers import UserSerializer, RegistrationSerializer

from email_validation.utils import verify_email

from permissions import IsValidEmail

import logging
logger = logging.getLogger('users')


class LoginView(views.APIView):
    permission_classes = (IsValidEmail,)
    serializer_class = UserSerializer

    def post(self, request):
        session_key = request.session.session_key
        username = request.data.get('username')
        password = request.data.get('password')
        user = auth.authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            if session_key:
                link_not_auth = Link.objects.filter(session_key=session_key)
                link_not_auth.user = user
                link_not_auth.session_key = None
                link_not_auth.save()
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(views.APIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
            request.session.flush()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Token.DoesNotExist:
            return Response({'message': 'there is no such token'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.debug(str(e))
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RegistrationView(views.APIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()

                verify_email(user=user, request=request)

                response_serializer = self.serializer_class(instance=user)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({'error': 'username is already taken'}, status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileViewSet(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.id)
