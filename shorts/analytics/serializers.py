from rest_framework.serializers import ModelSerializer
from .models import LinkStats


class LinkStatsSerializer(ModelSerializer):
    class Meta:
        model = LinkStats
        fields = '__all__'
