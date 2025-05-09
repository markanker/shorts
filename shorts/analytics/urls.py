from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import LinksAnalyticsViewSet

router = DefaultRouter()
router.register('stats', LinksAnalyticsViewSet, basename='stats')

urlpatterns = [
    path('', include(router.urls)),
]
