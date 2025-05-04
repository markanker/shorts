from django.shortcuts import redirect
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.mixins import DestroyModelMixin
from rest_framework import status
from rest_framework.response import Response

from . import serializers
from .models import Link

import logging
logger = logging.getLogger('links')


class LinksGetSourceView(GenericAPIView):
    lookup_field = 'short_link'

    def get_queryset(self):
        return Link.objects.all()

    def get(self, request, short_link):
        instance = self.get_object()
        # follower? analytics? statistics? is_owner?
        return redirect(instance.source_link)


class LinksListAddView(ListCreateAPIView):
    serializer_class = serializers.LinkSerializer
    """
    YO GOT NOT TO BE ABLE TO SET USER OR SESSION BY YOURSELF BUT THE CONTROLLER HAS
    """

    def get_queryset(self):
        return Link.objects.filter(user=self.request.user)


class LinksDeleteUpdate(DestroyModelMixin, GenericAPIView):
    serializer_class = serializers.LinkSerializer
    lookup_field = 'short_link'

    def get_queryset(self):
        return Link.objects.filter(user=self.request.user)

    def patch(self, request):
        instance = self.get_object()

        if len(request.data) != 1 or "short_link" not in request.data:
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
