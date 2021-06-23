# Generated by Django 3.2.4 on 2021-06-23 08:36

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Web', '0002_alter_chatroom_users'),
    ]

    operations = [
        migrations.CreateModel(
            name='WaitingRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='Waiting for chat', max_length=255)),
                ('users', models.ManyToManyField(blank=True, help_text='user thuoc waiting room', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]