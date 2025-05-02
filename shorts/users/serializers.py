from rest_framework import serializers
from users.models import User

import logging
logger = logging.getLogger('users')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'pfp')
        extra_kwargs = {
            'password': {'write_only': True, 'required': True, 'style': {'input_type': 'password'}},
            'pfp': {'required': False},
            'username': {'read_only': True}
        }

    def validate_pfp(self, pfp):
        logger.debug(f'type of the pfp is {type(pfp)}')
        return pfp

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = self.Meta.model(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
