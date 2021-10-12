#!/usr/bin/python
# -*- coding: UTF-8 -*-

from django import template

from monitoring.models import Zabbix

register = template.Library()

@register.filter(name='zarizeni_zabbix')
def zarizeni_zabbix(zarizeni, zabbix_id):
    return Zabbix.objects.filter(
            id=int(zabbix_id), 
            zarizeni=zarizeni).exists()