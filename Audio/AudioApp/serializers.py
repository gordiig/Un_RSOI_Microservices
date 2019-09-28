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
