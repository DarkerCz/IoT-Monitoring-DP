# Generated by Django 3.2.7 on 2021-10-14 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0015_auto_20211011_1508'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='zarizeni',
            name='trida',
        ),
        migrations.AlterField(
            model_name='data',
            name='jednotka',
            field=models.CharField(blank=True, choices=[('VOLTY', 'V'), ('STUPNE_C', '°C')], max_length=20, null=True, verbose_name='Jednotka'),
        ),
        migrations.AlterField(
            model_name='zabbix',
            name='zarizeni',
            field=models.ManyToManyField(related_name='zabbixs', to='monitoring.Zarizeni'),
        ),
    ]