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

    def update(self, instance: Image, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.width = validated_data.get('width', instance.width)
        instance.height = validated_data.get('height', instance.height)
        instance.save()
        return instance
