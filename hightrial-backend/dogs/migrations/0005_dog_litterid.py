# Generated by Django 4.1.2 on 2023-10-08 18:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dogs', '0004_remove_dog_litterid'),
    ]

    operations = [
        migrations.AddField(
            model_name='dog',
            name='litterID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dogs.litter'),
        ),
    ]
