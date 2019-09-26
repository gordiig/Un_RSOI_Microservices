from rest_framework import serializers
from MessagesApp.models import Message


class MessageSerializer(serializers.ModelSerializer):
    """
    Сериалиатор сообщения
    """
    class Meta:
        model = Message
        fields = [
            'uuid',
            'from_user_id',
            'to_user_id',
            'text',
            'image_uuid',
            'audio_uuid',
        ]

    def create(self, validated_data):
        new = Message.objects.create(**validated_data)
        return new
