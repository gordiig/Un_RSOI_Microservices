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

    def update(self, instance: Message, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.image_uuid = validated_data.get('image_uuid', instance.image_uuid)
        instance.audio_uuid = validated_data.get('audio_uuid', instance.audio_uuid)
        instance.save()
        return instance
