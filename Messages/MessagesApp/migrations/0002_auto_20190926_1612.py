# Generated by Django 2.2.4 on 2019-09-26 16:12

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('MessagesApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('c8f23dd5-ec5f-4b7a-98b8-c15f2e309599'), editable=False, primary_key=True, serialize=False),
        ),
    ]