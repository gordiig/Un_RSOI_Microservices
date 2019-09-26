from rest_framework import serializers
from MessagesApp.models import Message


class MessageSerializer(serializers.ModelSerializer):
    """
    Сериалиатор сообщения для списка (без подтягивания самого изображения и аудио)
    """
    has_image = serializers.SerializerMethodField()
    has_audio = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            'uuid',
            'text',
            'has_image',
            'has_audio',
        ]

    def get_has_image(self, instance: Message):
        return instance.image_uuid is not None

    def get_has_audio(self, instance: Message):
        return instance.audio_uuid is not None


class ConcreteMessageSerializer(MessageSerializer):
    """
    Сериализатор конкретного сообщения
    """
    image = serializers.SerializerMethodField()
    audio = serializers.SerializerMethodField()

    class Meta(MessageSerializer.Meta):
        fields = MessageSerializer.Meta.fields + [
            'image',
            'audio',
        ]

    def get_image(self, instance: Message):
        return self.context['image']

    def get_audio(self, instance: Message):
        return self.context['audio']
