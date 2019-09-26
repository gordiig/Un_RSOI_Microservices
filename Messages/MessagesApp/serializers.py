from rest_framework import serializers
from MessagesApp.models import Messages


class MessageSerializer(serializers.ModelSerializer):
    """
    Сериалиатор сообщения для списка (без подтягивания самого изображения и аудио)
    """
    class Meta:
        model =