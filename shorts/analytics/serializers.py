from rest_framework.serializers import ModelSerializer
from .models import LinkStats, Follower


class FollowerForSubscriberSerializer(ModelSerializer):
    class Meta:
        model = Follower
        fields = '__all__'


class FollowerPublicSerializer(ModelSerializer):
    class Meta:
        model = Follower
        exclude = ['city', 'ip_address']


class LinkStatsSerializer(ModelSerializer):
    follower = FollowerPublicSerializer()

    class Meta:
        model = LinkStats
        fields = '__all__'
