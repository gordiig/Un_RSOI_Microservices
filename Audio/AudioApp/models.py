import uuid
from django.db import models


class Audio(models.Model):
    """
    Модель аудио
    """
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256, null=False)
    length = models.IntegerField(null=False)

    def __str__(self):
        return self.name
