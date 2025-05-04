from django.shortcuts import redirect
from rest_framework.generics import GenericAPIView, get_object_or_404
from . import serializers
from .models import Link
from rest_framework.response import Response

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


class LinksListAddView(GenericAPIView):
    serializer_class = serializers.LinkSerializer

    def get_queryset(self):
        return Link.objects.all()

    def get(self, request):
        # return all the user's links
        pass

    def post(self, request):
        # return JSON
        pass


class LinksDeleteUpdate(GenericAPIView):
    serializer_class = serializers.LinkSerializer
    lookup_field = 'short_link'

    def patch(self, request, short_link):
        # return JSON
        pass

    def delete(self, request, short_link):
        # return JSON
        pass
