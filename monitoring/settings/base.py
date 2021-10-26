# -*- coding: UTF-8 -*-

# IP Adresa serveru (string)
IP_ADRESA = "#"

#UDP port (int)
PORT = 1700

# band - vyber z EU868, AU915, US915
BAND = 'EU868'

# DICT hodnot jako key v Zabbixu
HODNOTY_KEY_ZABBIX = {
    'NAPETI': 'napeti',
    'STAV_KONTAKTU': 'kontakt',
    'TEPLOTA': 'teplota'
}

DATA_KANAL = {
    3: 'NAPETI',
    1: 'STAV_KONTAKTU',
    2: 'TEPLOTA'
}

JEDNOTKA_KANAL = {
    3: 'VOLTY',
    2: 'STUPNE_C',
    1: None
}
