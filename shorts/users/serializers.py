from rest_framework import serializers
from users.models import User

from django.db.models.fields.files import ImageFieldFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from validators import get_validators_list

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

    def get_params_of_a_cropped_square(self, width, height):
        pivot = min(width, height)
        x = (width - height) // 2
        x = x if x >= 0 else 0
        y = (height - width) // 2
        y = y if y >= 0 else 0
        z = x + pivot
        w = y + pivot
        logging.debug(f'params of a square: {x}, {y}, {z}, {w}')
        return x, y, z, w

    def round_image(self, img, **kwargs):
        given = Image.open(img)
        cropped = given.crop(self.get_params_of_a_cropped_square(*given.size))
        resized = cropped.resize((200, 200))
        buffer = BytesIO()
        img_format = img.content_type[img.content_type.rfind('/') + 1:]
        resized.save(fp=buffer, quality=100, format=img_format)
        image_content_file = ContentFile(content=buffer.getvalue())
        return InMemoryUploadedFile(image_content_file, **kwargs)

    def validate_pfp(self, pfp):
        if not isinstance(pfp, ImageFieldFile):
            for validator in get_validators_list():
                validator(pfp)
            kwargs = {
                'charset': pfp.charset,
                'content_type': pfp.content_type,
                'field_name': pfp.field_name,
                'name': pfp.name,
                'size': pfp.size
            }
            pfp = self.round_image(pfp, **kwargs)
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


class RegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('id', 'username', 'password1', 'password2', 'email')

    def validate(self, data):
        if data['password1'] != data.pop('password2'):
            raise serializers.ValidationError("Passwords don't match")
        return data

    def create(self, validated_data):
        password = validated_data.pop('password1')
        user = self.Meta.model(**validated_data)
        user.set_password(password)
        user.save()
        return user

