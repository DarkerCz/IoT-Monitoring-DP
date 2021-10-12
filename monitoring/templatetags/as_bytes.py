#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re
from django import template

register = template.Library()

@register.filter(name='as_bytes')
def as_bytes(value):
    return " ".join(re.findall('([0-9A-F]{2}|[0-9A-F])', value))