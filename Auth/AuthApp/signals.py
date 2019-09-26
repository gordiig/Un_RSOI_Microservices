from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=User)
def create_token(sender, instance: User, created, *args, **kwargs):
    """
    Создаем токен после создания юзера
    :param sender: Класс User
    :param instance: Объект, который сохраняется
    :param created: True если создан, а не сохраняется
    """
    if created:
        Token.objects.create(user=instance)
