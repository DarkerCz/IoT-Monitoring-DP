# Generated by Django 3.2.6 on 2021-09-22 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0006_zprava_zarizeni'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gateway',
            name='port',
        ),
        migrations.RemoveField(
            model_name='zarizeni',
            name='appeui',
        ),
        migrations.RemoveField(
            model_name='zarizeni',
            name='otaa',
        ),
        migrations.RemoveField(
            model_name='zarizeni',
            name='tx_datr',
        ),
        migrations.RemoveField(
            model_name='zarizeni',
            name='tx_kanal',
        ),
        migrations.RemoveField(
            model_name='zprava',
            name='id_zpravy',
        ),
        migrations.AddField(
            model_name='gateway',
            name='lat',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='Latitude'),
        ),
        migrations.AddField(
            model_name='gateway',
            name='lon',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='Longitude'),
        ),
        migrations.AddField(
            model_name='zprava',
            name='typ_zpravy',
            field=models.IntegerField(blank=True, choices=[(0, 'Push data'), (1, 'Push acknowledge'), (2, 'Pull data'), (3, 'Pull response'), (4, 'Pull acknowledge')], null=True, verbose_name='Typ zprávy'),
        ),
    ]
