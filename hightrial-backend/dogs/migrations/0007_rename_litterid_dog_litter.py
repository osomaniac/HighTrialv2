# Generated by Django 4.1.2 on 2023-10-08 23:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dogs', '0006_remove_litter_litterid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dog',
            old_name='litterID',
            new_name='litter',
        ),
    ]