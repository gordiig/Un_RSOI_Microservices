from django.db import models


class Messages(models.Model):
    """
    Модель сообщения
    """
    uuid = models.UUIDField(primary_key=True)
    text = models.CharField(null=True, max_length=2048)
    image_uuid = models.UUIDField(null=True)
    audio_uuid = models.UUIDField(null=True)

    def __str__(self):
        return f'Message, uuid={self.uuid}'
