import json
import struct
import base64
import binascii
import random

from lora.crypto import loramac_decrypt
from python_cayennelpp.decoder import decode

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


def generuj_klic(delka):
    klic = random.getrandbits(delka)
    return format(klic, 'x').upper()


def generuj_nwkskey():
    nwkskey = None
    while not nwkskey:
        klic = generuj_klic(128)
        try:
            models.Zarizeni.objects.get(nwkskey=klic)
        except models.Zarizeni.DoesNotExist:
            nwkskey = klic
            return klic

def generuj_appskey():
    appskey = None
    while not appskey:
        klic = generuj_klic(128)
        try:
            models.Zarizeni.objects.get(appskey=klic)
        except models.Zarizeni.DoesNotExist:
            appskey = klic
            return klic

def decryptuj_data(data):
    try:
        zpracovana_data = zpracuj_data(data)
        if zpracovana_data:
            devaddr = zpracovana_data['devaddr']
            sequence_counter = int(zpracovana_data['fcnt'], 16)
            frm_payload = zpracovana_data['frm_payload']
            try:
                zarizeni = models.Zarizeni.objects.get(devaddr=devaddr)
            except models.Zarizeni.DoesNotExist:
                logger.info("Neznámé zařízení devaddr: {}".format(devaddr))
                return None
            key = zarizeni.appskey
            text = ""
            return loramac_decrypt(frm_payload, sequence_counter, key, devaddr)
        return None
    except Exception as e:
        logger.error("Chyba při decryptovani dat: {}".format(data))
        return None


def decoduj_cayenne_lpp(data):
    try:
        if type(data) != bytearray:
            data = bytearray(data)
        data = binascii.hexlify(data).decode('utf-8')
        return decode(data)
    except Exception as e:
        logger.error("Chyba při dekódování cayenne lpp: {}".format(data))
        return None


# decoduj payload data
def decoduj_payload_na_hex(payload):
    try:
        payload = json.loads(payload)['rxpk'][0]['data']
        return base64.b64decode(payload).hex().upper()
    except:
        return None

# zpracuj payload data
def zpracuj_data(hdata):
    try:
        x = "0x" + hdata[:2]
        typ = (int(x, 16) & 0xFF >> 5)
        if typ in (JOIN_REQUEST, UN_DATA_UP, CO_DATA_UP):
            # ( PHYPayload = MHDR[1] | MACPayload[..] | MIC[4] )
            mhdr = hdata[:2]
            mic = hdata[-8:]
            mac_payload = hdata[2:-8]
            # ( MACPayload = FHDR | FPort | FRMPayload )
            # ( FHDR = DevAddr[4] | FCtrl[1] | FCnt[2] | FOpts[0..15] )
            devaddr = to_little(mac_payload[:8])
            fctrl = mac_payload[8:10]
            fcnt = to_little(mac_payload[10:14])
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
                return None
            return {'mhdr': mhdr, 
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
        return None
    except Exception as e:
        logger.error("Chyba při zpracování dat zprávy - {}".format(e))
    return None

