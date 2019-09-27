import uuid
from django.db import models


class Image(models.Model):
    """
    Модель картинки
    """
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128, null=False)
    width = models.IntegerField()
    height = models.IntegerField()

    @property
    def extension(self):
        return self.name.split('.')[-1]

    @property
    def image_size(self):
        return f'{self.width}x{self.height}'

    def __str__(self):
        return self.name
