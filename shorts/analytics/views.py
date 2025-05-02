from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from links.models import Link
from users.models import User


class LinksAnalyticsView(GenericAPIView):
    def get(self, request, *args, **kwargs):
        pass

    def get_queryset(self):
        pass
