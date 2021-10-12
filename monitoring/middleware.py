# -*- coding: UTF-8 -*-

import simplejson

from django.contrib import messages
from django.utils.encoding import force_text


class AjaxMessaging(object):

    CONTENT_TYPES = ["application/javascript", "application/json"]
    TYPE_MAP = {
        messages.DEBUG: 'info',
        messages.INFO: 'info',
        messages.SUCCESS: 'success',
        messages.WARNING: 'warning',
        messages.ERROR: 'danger'}

    def __init__(self, get_response):
        self.get_response = get_response

    def get_message_dict(self, message):
        return {'message': force_text(message.message), 
            'type': self.TYPE_MAP.get(message.level)}

    def __call__(self, request):
        response = self.get_response(request)

        if request.is_ajax():
            if response['Content-Type'] in self.CONTENT_TYPES:
                try:
                    content = simplejson.loads(response.content)
                    assert isinstance(content, dict)
                except (ValueError, AssertionError):
                    return response

                content['django_messages'] = [self.get_message_dict(message)
                    for message in messages.get_messages(request)]

                response.content = simplejson.dumps(content)
        return response