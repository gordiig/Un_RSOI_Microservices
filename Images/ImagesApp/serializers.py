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
        ]

    def create(self, validated_data):
        width, height = validated_data['image_size'].split('x')
        new_image = Image.objects.create(**validated_data)
        new_image.width = width
        new_image.height = height
        new_image.save()
        return new_image
