from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import LinksAnalyticsViewSet, FollowerViewSet

router = DefaultRouter()
router.register('stats', LinksAnalyticsViewSet, basename='stats')
router.register('followers', FollowerViewSet, basename='followers')

urlpatterns = [
    path('', include(router.urls)),
]
