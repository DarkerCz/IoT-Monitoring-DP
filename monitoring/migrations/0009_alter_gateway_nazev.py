# Generated by Django 3.2.6 on 2021-09-23 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0008_auto_20210923_1351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gateway',
            name='nazev',
            field=models.CharField(blank=True, max_length=350, null=True, verbose_name='Název'),
        ),
    ]
