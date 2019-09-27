from rest_framework import serializers
from ImagesApp.models import Image


class ImageSerializer(serializers.ModelSerializer):
    """
    Сериализатор изображения
    """
    class Meta:
        model = Image
        fields = [
            'uuid',
            'name',
            'extension',
            'image_size',
            'width',
            'height'
        ]
        extra_kwargs = {
            'width': {'write_only': True},
            'height': {'write_only': True},
        }

    def create(self, validated_data):
        new_image = Image.objects.create(**validated_data)
        return new_image
