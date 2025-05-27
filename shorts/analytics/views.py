from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from .serializers import LinkStatsSerializer
from .models import Follower, LinkStats
from exceptions import ValidationError
from links.models import Link
from users.models import User
from .validators import FilterValidator

import logging
logger = logging.getLogger('analytics')


class LinksAnalyticsViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = LinkStatsSerializer
    lookup_field = 'short_link'

    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except ValidationError:
            return Response({'error': 'something'}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except ValidationError:
            return Response({'error': 'something'}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        owner = self.request.GET.get('owner')
        device = self.request.GET.get('device', 'pc')
        country = self.request.GET.get('country')
        city = self.request.GET.get('city')
        time = self.request.GET.get('time')
        from_time = self.request.GET.get('from_time')
        to_time = self.request.GET.get('to_time')
        browser = self.request.GET.get('browser')
        followers = self.request.GET.get('followers', 'all')

        try:
            validator = FilterValidator(
                owner=owner,
                device=device,
                time=time,
                from_time=from_time,
                to_time=to_time,
                browser=browser,
                followers=followers,
                country=country,
                city=city
            )
        except ValidationError as ve:
            logger.exception(str(ve))
            raise ValidationError(str(ve))

        return LinkStats.objects.select_related('link', 'follower').filter(**validator.filter_kwargs)
