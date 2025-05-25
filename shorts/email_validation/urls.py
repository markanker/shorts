from django.urls import path
from .views import verify_email_view, send_again_view
from django.urls import register_converter
from .converters import CodeConverter

register_converter(CodeConverter, 'verif_code')

urlpatterns = [
    path('<verif_code:verif_code>/', verify_email_view, name='verify-email'),
    path('send_again/', send_again_view, name='send-again'),
]
