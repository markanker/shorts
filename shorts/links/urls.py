from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from django.urls import register_converter
from .converters import ShortLinkConverter

register_converter(ShortLinkConverter, 'shorts')

router = DefaultRouter()

urlpatterns = [
    path('<shorts:short_link>/', views.LinksGetSourceView.as_view()),  # /{regular_expression}/ [GET]
    path('links/<shorts:short_link>/', views.LinksGetSourceView.as_view()),  # /links/{id} [PATCH, DELETE]
    path('links/', views.LinksGetSourceView.as_view()),  # /links/ [POST, GET]
]
