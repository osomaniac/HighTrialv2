# Generated by Django 4.1.2 on 2022-11-05 16:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dogs', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dog',
            name='kennel',
        ),
        migrations.AddField(
            model_name='dog',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
