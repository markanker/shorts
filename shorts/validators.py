from django.core.exceptions import ValidationError
from PIL import Image


def validate_image_type(image):
    if image:
        if image.content_type not in {'image/png', 'image/jpg', 'image/jpeg'}:
            raise ValidationError('Неверный формат изображения')


def validate_image_integrity(image):
    if image:
        try:
            img = Image.open(image)
            img.verify()
        except IOError:
            raise ValidationError('Загруженный файл содержит вредоносный код')


def get_validators_list():
    return [validate_image_type, validate_image_integrity]
