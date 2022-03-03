import json
import struct
import base64
import binascii
import random

from lora.crypto import loramac_decrypt
from python_cayennelpp.decoder import decode
from pyzabbix import ZabbixMetric, ZabbixSender

from monitoring import settings as app_settings
from . import models

import logging
logger = logging.getLogger(__name__)


JOIN_REQUEST = 0
JOIN_ACCEPT = 1
UN_DATA_UP = 2
UN_DATA_DOWN = 3
CO_DATA_UP = 4
CO_DATA_DOWN = 5
REV = 6
PROPRIETARY = 7


def to_little(val):
    little_hex = bytearray.fromhex(val)
    little_hex.reverse()
    str_little = ''.join(format(x, '02x') for x in little_hex)
    return str_little.upper()


def generuj_unikatni_klic(attr, delka):
    while True:
        klic = format(random.getrandbits(delka), 'x').upper()
        try:
            models.Zarizeni.objects.get(**{attr: klic})
        except models.Zarizeni.DoesNotExist:
            return klic


def decryptuj_data(zprava):
    if zprava.zarizeni and zprava.fcnt:
        zarizeni = zprava.zarizeni
        devaddr = zprava.devaddr
        sequence_counter = int(zprava.fcnt, 16)
        key = zarizeni.appskey
        frm_payload = zprava.frm_payload
        return loramac_decrypt(frm_payload, sequence_counter, key, devaddr)
    return False


def decoduj_cayenne_lpp(data):
    try:
        if type(data) != bytearray:
            data = bytearray(data)
        data = binascii.hexlify(data).decode('utf-8')
        return decode(data)
    except Exception as e:
        logger.error("Chyba při dekódování cayenne lpp: {}".format(data))
        return False


def over_konzistenci_dat(data, zprava):
    delka = getattr(app_settings, 'POCET_CAYENNE_HODNOT', 3)
    limity = getattr(app_settings, 'LIMITY_KANAL')
    if len(data) != delka:
        logger.error("Nekonzistentní data zprávy PK: {} ze zařízení PK: {}, nesprávná délka {} != {}".format(zprava.pk, zprava.zarizeni.pk, len(data), delka))
        return False
    else:
        for hodnota in data:
            try:
                if limity[hodnota['channel']][0] <= hodnota['value'] <= limity[hodnota['channel']][1]:
                    pass
                else:
                    logger.error("Nekonzistentní data zprávy PK: {} ze zařízení PK: {}, data pro kanál {} mimo rozsah {} <> {}".format(zprava.pk, zprava.zarizeni.pk, hodnota['channel'], hodnota['value'], limity[hodnota['channel']]))
                    return False
            except KeyError:
                logger.error("Nekonzistentní data zprávy PK:{}, neznámý kanál {}".format(zprava.pk, hodnota['channel']))
                return False
    return True

            
# decoduj payload data
def decoduj_payload_na_hex(payload):
    try:
        payload = json.loads(payload)['rxpk'][0]['data']
        return base64.b64decode(payload).hex().upper()
    except:
        return False

# zpracuj payload data
def zpracuj_data(hdata):
    try:
        mhdr = hdata[:2]
        typ = (int(mhdr, 16) & 224) >> 5
        if typ in (UN_DATA_UP, CO_DATA_UP):
            # ( PHYPayload = MHDR[1] | MACPayload[..] | MIC[4] )
            mic = hdata[-8:]
            mac_payload = hdata[2:-8]
            # ( MACPayload = FHDR | FPort | FRMPayload )
            # ( FHDR = DevAddr[4] | FCtrl[1] | FCnt[2] | FOpts[0..15] )
            devaddr = to_little(mac_payload[:8])
            fctrl = mac_payload[8:10]
            fcnt = to_little(mac_payload[10:14])
            if fcnt:
                fopts_len = (int('0x'+fctrl, 16) & 15)*2
                fopts = mac_payload[14:14+fopts_len]
                fhdr_len = 14 + fopts_len
                fhdr = mac_payload[0:fhdr_len]
                fport = mac_payload[fhdr_len:fhdr_len+2]
                frm_payload = mac_payload[fhdr_len+2:]
                try:
                    zarizeni = models.Zarizeni.objects.get(devaddr=devaddr)
                except models.Zarizeni.DoesNotExist:
                    logger.info("Neznámé zařízení devaddr: {}".format(devaddr))
                    return False
                return {'typ_zpravy_MAC': typ,
                        'mhdr': mhdr, 
                        'mic': mic,
                        'mac_payload': mac_payload,
                        'devaddr': devaddr,
                        'fctrl': fctrl,
                        'fcnt': fcnt,
                        'fopts': fopts,
                        'fhdr': fhdr,
                        'fport': fport,
                        'frm_payload': frm_payload
                        }
        return False
    except Exception as e:
        logger.error("Chyba při zpracování dat zprávy - {}".format(e))
    return False


def odesli_data_zabbixu(data, zabbix):
    zbx = ZabbixSender(zabbix.ip_adresa, zabbix.port)
    metrics = []
    metric = ZabbixMetric(
        data.zarizeni.nazev, 
        app_settings.HODNOTY_KEY_ZABBIX[data.typ_hodnoty], 
        data.hodnota, 
        data.zprava.created.timestamp()
    )
    metrics.append(metric)
    status = zbx.send(metrics)
    return bool(not status.failed)
