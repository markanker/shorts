from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import DestroyModelMixin
from rest_framework.response import Response
from rest_framework import status

from django.urls import NoReverseMatch
from django.db.utils import IntegrityError

from django.shortcuts import redirect
from . import serializers
from .models import Link

from random import choices, randint
from string import ascii_letters, digits

import logging
logger = logging.getLogger('links')

RANDOM_LINK_CHARS = ascii_letters + digits + '-_'


class LinksGetSourceView(GenericAPIView):
    lookup_field = 'short_link'

    def get_queryset(self):
        return Link.objects.all()

    def get(self, request, short_link):
        instance = self.get_object()
        # follower? analytics? statistics? is_owner?
        try:
            response = redirect(instance.source_link)
        except NoReverseMatch:
            response = Response({'source_link': instance.source_link},
                                status=status.HTTP_200_OK)
        return response


class LinksListAddView(ListCreateAPIView):
    serializer_class = serializers.LinkSerializer
    """
    YO GOT NOT TO BE ABLE TO SET USER OR SESSION BY YOURSELF BUT THE CONTROLLER HAS
    """

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        if not (request.user.is_authenticated and data.get('short_link')):
            data['short_link'] = ''.join(choices(RANDOM_LINK_CHARS, k=randint(5, 15)))
        if request.user.is_authenticated:
            data['user'] = request.user.id
        else:
            data['session_key'] = 'I dont know for now'
        try:
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
        except IntegrityError as ie:
            logger.exception(str(ie))
            return Response({'message': 'this short name for a link is already taken, try again with another one'},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        return Link.objects.filter(user=self.request.user.id)


class LinksDeleteUpdate(DestroyModelMixin, GenericAPIView):
    serializer_class = serializers.LinkSerializer
    lookup_field = 'short_link'

    def get_queryset(self):
        return Link.objects.filter(user=self.request.user)

    def patch(self, request):
        instance = self.get_object()

        if not (len(request.data) >= 1 and "short_link" in request.data):
            return Response(
                {'message': 'it is only possible to change short_link field and not other'},
                status=status.HTTP_406_NOT_ACCEPTABLE
            )

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
