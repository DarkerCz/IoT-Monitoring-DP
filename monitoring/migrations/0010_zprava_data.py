# Generated by Django 3.2.6 on 2021-09-24 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0009_alter_gateway_nazev'),
    ]

    operations = [
        migrations.AddField(
            model_name='zprava',
            name='data',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='Data'),
        ),
    ]
