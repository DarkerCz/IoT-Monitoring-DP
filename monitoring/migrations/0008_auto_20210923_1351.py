# Generated by Django 3.2.6 on 2021-09-23 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0007_auto_20210922_1349'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gateway',
            old_name='jmeno',
            new_name='nazev')
    ]
