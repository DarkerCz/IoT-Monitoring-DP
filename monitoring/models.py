# -*- coding: UTF-8 -*-

import struct
import json
import base64
import binascii
import datetime

from uuid import uuid4

from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.models import TimeStampedModel

from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save

from django.core.validators import MaxValueValidator, MinValueValidator



from . import utils
from monitoring import settings as app_settings

import logging
logger = logging.getLogger(__name__)

PUSH_DATA = 0
PUSH_ACK = 1
PULL_DATA = 2
PULL_RESP = 3
PULL_ACK = 4
TX_ACK = 5

class Gateway(TimeStampedModel):

    uuid = models.UUIDField(unique=True, default=uuid4, editable=False)
    ip_adresa = models.CharField('IP adresa', max_length=14, blank=True, null=True)
    nazev = models.CharField('Název', max_length=350, blank=True, null=True)
    eui = models.CharField('Gateway EUI', max_length=50, blank=True, null=True)
    lat = models.DecimalField('Latitude', max_digits=9, decimal_places=6, blank=True, null=True)
    lon = models.DecimalField('Longitude', max_digits=9, decimal_places=6, blank=True, null=True)
    povolena = models.BooleanField('Povolena', default=True)

    class Meta:
        verbose_name = 'Gateway'
        verbose_name_plural = 'Gateways'
        ordering = ('-created',)

@receiver(pre_save, sender=Gateway)
def Gateway_pre_save_handler(sender, instance, **kwargs):
    instance.eui = instance.eui.upper()


class Zarizeni(TimeStampedModel):

    uuid = models.UUIDField(unique=True, default=uuid4, editable=False)
    nazev = models.CharField('Název', max_length=128, blank=True, null=True)
    devaddr = models.CharField('DevAddr', max_length=128, blank=True, null=True)
    deveui = models.CharField('DevEUI', max_length=128, blank=True, null=True)
    nwkskey = models.CharField('NwkSKey', max_length=128, blank=True, null=True)
    appskey = models.CharField('AppSKey', max_length=128, blank=True, null=True)
    povoleno = models.BooleanField('Povoleno', default=True)

    class Meta:
        verbose_name = 'Zařízení'
        verbose_name_plural = 'Zařízení'
        ordering = ('-created',)



class Zprava(TimeStampedModel):

    TX = 'TX'
    RX = 'RX'

    SMERY = (
        (TX, 'TX - Odeslána'),
        (RX, 'RX - Přijata'),
    )

    TYPY_ZPRAV = (
        (PUSH_DATA, 'Push data'),
        (PUSH_ACK, 'Push acknowledge'),
        (PULL_DATA, 'Pull data'),
        (PULL_RESP, 'Pull response'),
        (PULL_ACK, 'Pull acknowledge'),
    )

    gateway = models.ForeignKey(Gateway, related_name='zpravy', verbose_name='Gateway',
        blank=True, null=True, on_delete=models.SET_NULL)

    zarizeni = models.ForeignKey(Zarizeni, related_name='zpravy', verbose_name='Zarizeni',
        blank=True, null=True, on_delete=models.SET_NULL)

    uuid = models.UUIDField(unique=True, default=uuid4, editable=False)
    typ_zpravy = models.IntegerField('Typ zprávy', choices=TYPY_ZPRAV, blank=True, null=True)
    verze = models.PositiveIntegerField('Verze', blank=True, null=True)
    token = models.CharField('Token', max_length=128, blank=True, null=True)
    payload = models.CharField('Payload', max_length=1024, blank=True, null=True)
    hex_data = models.CharField('HEX Data', max_length=1024, blank=True, null=True)
    data = models.CharField('Data', max_length=1024, blank=True, null=True)
    mic = models.CharField('MIC', max_length=32, blank=True, null=True)
    ip_adresa = models.CharField('IP adresa', max_length=14, blank=True, null=True)
    port = models.PositiveIntegerField('Port', blank=True, null=True)
    smer = models.CharField('Směr zprávy', choices=SMERY, max_length=2, blank=True, null=True)

    class Meta:
        verbose_name = 'Zpráva'
        verbose_name_plural = 'Zprávy'
        ordering = ('-created',)

    def push_ack_zprava(self):
        push_ack_zprava = Zprava.objects.create(typ_zpravy = PUSH_ACK, verze = self.verze, token = self.token, ip_adresa = self.ip_adresa, port = self.port, smer = 'TX', zarizeni = self.zarizeni, gateway = self.gateway)
        return push_ack_zprava

    def push_ack_packet(self):
        push_ack_zprava = self.push_ack_zprava()
        packet = struct.pack('<BHB', push_ack_zprava.verze, int(push_ack_zprava.token), int(push_ack_zprava.typ_zpravy))
        return packet

    def pull_ack_zprava(self):
        pull_ack_zprava = Zprava.objects.create(typ_zpravy = PULL_ACK, verze = self.verze, token = self.token, ip_adresa = self.ip_adresa, port = self.port, smer = 'TX', gateway = self.gateway)
        return pull_ack_zprava

    def pull_ack_packet(self):
        pull_ack_zprava = self.pull_ack_zprava()
        packet = struct.pack('<BHBp', pull_ack_zprava.verze, int(pull_ack_zprava.token), int(pull_ack_zprava.typ_zpravy), bytes(pull_ack_zprava.gateway.eui, 'utf-8'))
        return packet

    def decoduj_payload_data_na_hex(self):
        try:
            payload = json.loads(self.payload)['rxpk'][0]['data']
            self.hex_data = base64.b64decode(payload).hex().upper()
            self.save()
            return self.hex_data
        except Exception:
            return None
    
    def json_payload(self):
        try:
            data = json.loads(self.payload)['rxpk'][0]['data']
            return data
        except Exception:
            return None
    
    def je_duplicitni(self):
        if Zprava.objects.filter(mic=self.mic, created__gte=now() - datetime.timedelta(seconds = 60)).exclude(pk=self.pk).count() > 1:
            return True
        return False
    
    def prirad_zarizeni(self, zarizeni):
        if not self.zarizeni:
            self.zarizeni = zarizeni
            self.save()
        else:
            if self.zarizeni != zarizeni:
                logger.error("Pokus o přiřazení zařízení ke zprávě pk: {} u které je jiné zařízení".format(self.pk))

    def text_data(self):
        if self.data_hodnoty.exists():
            hodnoty = []
            for hodnota in self.data_hodnoty.all().order_by('typ_hodnoty'):
                hodnoty.append(hodnota.__str__())
            return "; ".join(hodnoty)
        else:
            return None

    def zpracuj_data(self):
        try:
            if self.hex_data:
                decryptovana_data = None
                decryptovana_data = utils.decryptuj_data(self.hex_data)
                if decryptovana_data:
                    zpracovana_data = utils.decoduj_cayenne_lpp(decryptovana_data)
                    if zpracovana_data:
                        for hodnota in zpracovana_data:
                            data, created = Data.objects.get_or_create(zarizeni = self.zarizeni, 
                                zprava= self, hodnota=hodnota['value'], 
                                typ_hodnoty = app_settings.DATA_KANAL[hodnota['channel']], 
                                jednotka = app_settings.JEDNOTKA_KANAL[hodnota['channel']],
                            )
                        return self.data_hodnoty.all()
            return None
        except Exception as e:
            logger.error("Chyba pri zpracovani dat zpravy pk: {}".format(self.pk))


@receiver(post_save, sender=Zprava)
def Zprava_post_save_handler(sender, instance, created, **kwargs):
    if created:
        instance.zpracuj_data()


class Data(TimeStampedModel):

    VOLTY = 'VOLTY'
    STUPNE_C = 'STUPNE_C'

    NAPETI = 'NAPETI'
    TEPLOTA = 'TEPLOTA'
    STAV_KONTAKTU = 'STAV_KONTAKTU'

    JEDNOTKY = (
        (VOLTY, 'V'),
        (STUPNE_C, '°C'),
    )

    TYPY_HODNOT = (
        (NAPETI, 'Napětí'),
        (TEPLOTA, 'Teplota'),
        (STAV_KONTAKTU, 'Stav kontaktu'),
    )

    zprava = models.ForeignKey(Zprava, related_name='data_hodnoty', verbose_name='data_hodnoty',
        blank=True, null=True, on_delete=models.SET_NULL)

    zarizeni = models.ForeignKey(Zarizeni, related_name='data_hodnoty', verbose_name='data_hodnoty',
        blank=True, null=True, on_delete=models.SET_NULL)

    uuid = models.UUIDField(unique=True, default=uuid4, editable=False)

    hodnota = models.DecimalField('Hodnota', max_digits=5, decimal_places=2, blank=True, null=True)

    typ_hodnoty = models.CharField('Typ hodnoty', choices=TYPY_HODNOT, max_length=20, blank=True, null=True)
    jednotka = models.CharField('Jednotka', choices=JEDNOTKY, max_length=20, blank=True, null=True)

    class Meta:
        verbose_name = 'Data'
        verbose_name_plural = 'Data'
        ordering = ('-created',)

    def __str__(self):
        return "{}: {}{}{}".format(self.get_typ_hodnoty_display(), self.render_hodnota, " " if self.jednotka else "", self.get_jednotka_display() if self.jednotka else "")

    @property
    def render_hodnota(self):
        if self.jednotka:
            return self.hodnota
        elif self.hodnota:
            return _("Spojeno")
        else:
            return _("Rozpojeno")


class Zabbix(TimeStampedModel):

    zarizeni = models.ManyToManyField(Zarizeni, related_name='zarizeni')

    uuid = models.UUIDField(unique=True, default=uuid4, editable=False)

    nazev = models.CharField('Název', max_length=128, blank=True, null=True)
    ip_adresa = models.CharField('IP adresa', max_length=14)
    port = models.PositiveIntegerField('Port', default="10051", validators=[MinValueValidator(0), MaxValueValidator(65535)])
    povolen = models.BooleanField('Povolen', default=True)

    class Meta:
        verbose_name = 'Zabbix'
        verbose_name_plural = 'Zabbix'
        ordering = ('-created',)

