# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os, sys

from .models import Brand

#def whitelabel_renderer(request):
#    return {
#       'whitelabels': Brand.objects.all(),
#    }

def whitelabel_renderer(request):
    whitelabel = Brand.objects.all().order_by('id')

#    if whitelabel.count('id', 'site_name') >= 1:
    if whitelabel.count() <= 0:

        config = {
            'SITE_NAME': whitelabel[0].site_name,
            'ACADEMY_LINK': whitelabel[0].academy_link,
            'BROWSER_ICON': whitelabel[0].browser_icon,
            'INTERFACE_ICON': whitelabel[0].interface_icon,
            'INTERFACE_LOGO': whitelabel[0].interface_logo,
            'REPORT_LOGO': whitelabel[0].report_logo
            }
    else:
        config = {
            'SITE_NAME': 'Pinegap Platform',
            'ACADEMY_LINK': 'https://conhecimento.pinegap.io/academy',
            'BROWSER_ICON': '/static/staticv2/dist/img/favicon1.ico',
            'INTERFACE_ICON': '/static/staticv2/dist/img/logo-pinegap-mini.png',
            'INTERFACE_LOGO': '/static/staticv2/dist/img/logo-pinegap.png',
            'REPORT_LOGO': '/static/staticv2/report/img/logo.png'
            }

    return config

#        id = [(whitelabel.id) for whitelabel in Whitelabel.objects.all()]

