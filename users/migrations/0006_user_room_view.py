# Generated by Django 3.2.4 on 2021-06-24 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0004_chatroom_view_users'),
        ('users', '0005_user_room_chat'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='room_view',
            field=models.ManyToManyField(blank=True, help_text='user only view', related_name='Viewer', to='Web.ChatRoom'),
        ),
    ]
