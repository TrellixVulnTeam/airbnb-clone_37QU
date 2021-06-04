# Generated by Django 3.2.3 on 2021-06-04 08:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0003_alter_room_host'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lists', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='list',
            name='rooms',
            field=models.ManyToManyField(blank=True, related_name='List_rooms', to='rooms.Room'),
        ),
        migrations.AlterField(
            model_name='list',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='List_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
