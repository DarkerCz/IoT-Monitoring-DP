# Generated by Django 3.2.7 on 2022-03-07 14:48

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('hodnota', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Hodnota')),
                ('typ_hodnoty', models.CharField(blank=True, choices=[('NAPETI', 'Napětí'), ('TEPLOTA', 'Teplota'), ('STAV_KONTAKTU', 'Stav kontaktu')], max_length=20, null=True, verbose_name='Typ hodnoty')),
                ('jednotka', models.CharField(blank=True, choices=[('VOLTY', 'V'), ('STUPNE_C', '°C')], max_length=20, null=True, verbose_name='Jednotka')),
            ],
            options={
                'verbose_name': 'Data',
                'verbose_name_plural': 'Data',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Gateway',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('ip_adresa', models.CharField(blank=True, max_length=14, null=True, verbose_name='IP adresa')),
                ('nazev', models.CharField(max_length=350, verbose_name='Název')),
                ('eui', models.CharField(max_length=50, unique=True, verbose_name='Gateway EUI')),
                ('lat', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='Latitude')),
                ('lon', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='Longitude')),
                ('povolena', models.BooleanField(default=True, verbose_name='Povolena')),
            ],
            options={
                'verbose_name': 'Gateway',
                'verbose_name_plural': 'Gateways',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Zabbix',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('nazev', models.CharField(blank=True, max_length=128, null=True, verbose_name='Název')),
                ('ip_adresa', models.CharField(max_length=14, verbose_name='IP adresa')),
                ('port', models.PositiveIntegerField(default='10051', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(65535)], verbose_name='Port')),
                ('povolen', models.BooleanField(default=True, verbose_name='Povolen')),
            ],
            options={
                'verbose_name': 'Zabbix',
                'verbose_name_plural': 'Zabbix',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Zarizeni',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('nazev', models.CharField(max_length=128, verbose_name='Název')),
                ('devaddr', models.CharField(max_length=128, verbose_name='DevAddr')),
                ('deveui', models.CharField(max_length=128, unique=True, verbose_name='DevEUI')),
                ('nwkskey', models.CharField(max_length=128, verbose_name='NwkSKey')),
                ('appskey', models.CharField(max_length=128, verbose_name='AppSKey')),
                ('povoleno', models.BooleanField(default=True, verbose_name='Povoleno')),
            ],
            options={
                'verbose_name': 'Zařízení',
                'verbose_name_plural': 'Zařízení',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Zprava',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('typ_zpravy_GWMP', models.IntegerField(blank=True, choices=[(0, 'Push data'), (1, 'Push acknowledge'), (2, 'Pull data'), (3, 'Pull response'), (4, 'Pull acknowledge')], null=True, verbose_name='Typ zprávy GWMP')),
                ('typ_zpravy_MAC', models.IntegerField(blank=True, choices=[(0, 'Join request'), (1, 'Join accept'), (2, 'Unconfirmed data UP'), (3, 'Unconfirmed data DOWN'), (4, 'Confirmed data UP'), (5, 'Confirmed data DOWN'), (7, 'Proprietary')], null=True, verbose_name='Typ zprávy MAC Message')),
                ('verze', models.PositiveIntegerField(blank=True, null=True, verbose_name='Verze')),
                ('token', models.CharField(blank=True, max_length=128, null=True, verbose_name='Token')),
                ('payload', models.CharField(blank=True, max_length=1024, null=True, verbose_name='Payload')),
                ('hex_data', models.CharField(blank=True, max_length=1024, null=True, verbose_name='HEX Data')),
                ('data', models.CharField(blank=True, max_length=1024, null=True, verbose_name='Data')),
                ('ip_adresa', models.CharField(blank=True, max_length=14, null=True, verbose_name='IP adresa')),
                ('port', models.PositiveIntegerField(blank=True, null=True, verbose_name='Port')),
                ('smer', models.CharField(blank=True, choices=[('TX', 'TX - Odeslána'), ('RX', 'RX - Přijata')], max_length=2, null=True, verbose_name='Směr zprávy')),
                ('mhdr', models.CharField(blank=True, max_length=16, null=True, verbose_name='MHDR')),
                ('mic', models.CharField(blank=True, max_length=16, null=True, verbose_name='MIC')),
                ('mac_payload', models.CharField(blank=True, max_length=256, null=True, verbose_name='MAC Payload')),
                ('devaddr', models.CharField(blank=True, max_length=16, null=True, verbose_name='Adresa zařízení')),
                ('fctrl', models.CharField(blank=True, max_length=16, null=True, verbose_name='FCtrl')),
                ('fcnt', models.CharField(blank=True, max_length=16, null=True, verbose_name='FCnt')),
                ('fopts', models.CharField(blank=True, max_length=16, null=True, verbose_name='FOpts')),
                ('fhdr', models.CharField(blank=True, max_length=128, null=True, verbose_name='FHDR')),
                ('fport', models.CharField(blank=True, max_length=16, null=True, verbose_name='FPort')),
                ('frm_payload', models.CharField(blank=True, max_length=128, null=True, verbose_name='FRM payload')),
                ('gateway', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='zpravy', to='monitoring.gateway', verbose_name='Gateway')),
                ('zarizeni', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='zpravy', to='monitoring.zarizeni', verbose_name='Zarizeni')),
            ],
            options={
                'verbose_name': 'Zpráva',
                'verbose_name_plural': 'Zprávy',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='ZabbixSenderLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('odeslano', models.BooleanField(default=True, verbose_name='Odesláno')),
                ('data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender_log', to='monitoring.data')),
                ('zabbix', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender_log', to='monitoring.zabbix')),
            ],
            options={
                'verbose_name': 'ZabbixSender log',
                'verbose_name_plural': 'ZabbixSender logy',
                'ordering': ('-created',),
            },
        ),
        migrations.AddField(
            model_name='zabbix',
            name='zarizeni',
            field=models.ManyToManyField(related_name='zabbixs', to='monitoring.Zarizeni'),
        ),
        migrations.AddField(
            model_name='data',
            name='zarizeni',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='data_hodnoty', to='monitoring.zarizeni', verbose_name='data_hodnoty'),
        ),
        migrations.AddField(
            model_name='data',
            name='zprava',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='data_hodnoty', to='monitoring.zprava', verbose_name='data_hodnoty'),
        ),
    ]
