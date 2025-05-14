from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from django.urls import register_converter
from .converters import ShortLinkConverter

register_converter(ShortLinkConverter, 'shorts')

router = DefaultRouter()

urlpatterns = [
    path('api/links/', views.LinksListAddView.as_view()),  # /links/ [POST, GET]
    path('api/links/<shorts:short_link>/', views.LinksDeleteUpdate.as_view()),  # /links/{short_link} [PATCH, DELETE]
    path('<shorts:short_link>/', views.LinksGetSourceView.as_view()),  # /{regular_expression}/ [GET]
]
