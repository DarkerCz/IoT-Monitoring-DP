# -*- coding: UTF-8 -*-

import socket
import struct
import json
import base64
import binascii

from django.core.management.base import BaseCommand, CommandError

from monitoring.models import Gateway, Zprava, Zarizeni
from monitoring import settings as app_settings

from monitoring.utils import to_little, decoduj_payload_na_hex, zpracuj_data

import logging
logger = logging.getLogger(__name__)

class Command(BaseCommand):

    args = ''

    def handle(self, *args, **options):

        # Definice socket serveru
        IP_ADRESA = getattr(app_settings, "IP_ADRESA")
        PORT = getattr(app_settings, "PORT")

        # Typy paketů
        PUSH_DATA = 0
        PUSH_ACK = 1
        PULL_DATA = 2
        PULL_RESP = 3
        PULL_ACK = 4
        TX_ACK = 5

        # Spuštění serveru
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((IP_ADRESA, PORT))

        # PULL ACK odpověď
        def odeslat_pull_ack(verze, token, gatewayEUI, ip_adresa, port):
            packet = struct.pack('<BHBp', verze, int(token), PULL_ACK, bytes(gatewayEUI, 'utf-8'))
            sock.sendto(packet, (ip_adresa, port))

        # PUSH ACK odpověď
        def odeslat_push_ack(prijata_zprava):
            sock.sendto(prijata_zprava.push_ack_packet(), (prijata_zprava.ip_adresa, prijata_zprava.port))


        while True:
            zpracovana_data = None
            data, addr = sock.recvfrom(1024)
            print("received message from {}: {}".format(addr, data))
            (verze, token, typ_zpravy) = struct.unpack('<BHB', data[:4])
            gatewayEUI = binascii.hexlify(data[4:12]).decode("utf-8")
            try: 
                gateway = Gateway.objects.get(eui=gatewayEUI.upper(), povolena=True)
            except Exception as e:
                gateway = None
                logger.warning("Neznámá nebo zakázaná brána s EUI: {}".format(gatewayEUI))
            if gateway:        
                if ( typ_zpravy in (1, 2) or 
                        verze == 1 and typ_zpravy in (PUSH_DATA, PULL_DATA) 
                        or 
                        verze == 2 and typ_zpravy in (PUSH_DATA, PULL_DATA, TX_ACK)
                        ):
                    if typ_zpravy == PUSH_DATA:
                        if len(data) < 12:
                            logger.error("Délka zprávy PUSH_DATA je kratší než minimální délka 12")
                        else:
                            print("PUSH_DATA")
                        hex_data = decoduj_payload_na_hex(data[12:].decode("utf-8"))
                        if hex_data:
                            zpracovana_data = zpracuj_data(hex_data)
                        if zpracovana_data:
                            zarizeni = Zarizeni.objects.get(devaddr=zpracovana_data['devaddr'])
                            zpracovana_data['gateway'] = gateway
                            zpracovana_data['typ_zpravy'] = typ_zpravy
                            zpracovana_data['verze'] = verze
                            zpracovana_data['token'] = token
                            zpracovana_data['ip_adresa'] = addr[0]
                            zpracovana_data['port'] = addr[1]
                            zpracovana_data['smer'] = 'RX'
                            zpracovana_data['payload'] = data[12:].decode("utf-8")
                            zpracovana_data['hex_data'] = hex_data
                            zpracovana_data['zarizeni'] = zarizeni
                            zprava = Zprava(**zpracovana_data)
                            zprava.save()
                            odeslat_push_ack(zprava)
                    elif typ_zpravy == PULL_DATA:
                        if len(data) < 12:
                            logger.error("Délka zprávy PULL_DATA je kratší než minimální délka 12")
                        else:
                            print("PULL_DATA")
                            odeslat_pull_ack(verze, token, gatewayEUI, addr[0], addr[1])
                else:
                    logger.warning("Nepodporovaný typ zprávy: {} a verze: {}".format(typ_zpravy, verze))