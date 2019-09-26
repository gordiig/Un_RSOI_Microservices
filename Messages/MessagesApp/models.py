import uuid
from django.db import models


class Message(models.Model):
    """
    Модель сообщения
    """
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    from_user_id = models.IntegerField(null=False)
    to_user_id = models.IntegerField(null=False)
    text = models.CharField(null=True, max_length=2048)
    image_uuid = models.UUIDField(null=True)
    audio_uuid = models.UUIDField(null=True)

    def __str__(self):
        return f'Message, uuid={self.uuid}'
