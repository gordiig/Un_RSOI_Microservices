from rest_framework import serializers
from AudioApp.models import Audio


class AudioSerializer(serializers.ModelSerializer):
    """
    Сериализатор аудио
    """
    class Meta:
        model = Audio
        fields = [
            'uuid',
            'name',
            'length',
        ]

    def create(self, validated_data):
        new = Audio.objects.create(**validated_data)
        return new

    def update(self, instance: Audio, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.length = validated_data.get('length', instance.length)
        instance.save()
        return instance
