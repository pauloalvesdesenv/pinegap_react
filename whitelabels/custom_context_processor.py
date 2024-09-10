# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os, sys
from .models import Brand


def whitelabel_renderer(request):
     whitelabel = Brand.objects.all().order_by('id')

     if whitelabel.count() == 0:

        config = {
            'site_name': 'Pinegap Platform',
            'academy_link': 'https://conhecimento.pinegap.io/',
            'browser_icon': 'default_logos/dist/img/favicon1.ico',
            'interface_icon': 'default_logos/dist/img/logo-pinegap-mini.png',
            'interface_logo': 'default_logos/dist/img/logo-pinegap.png',
            'report_logo': 'default_logos/reports/img/logo.png'
	    }
     else:

        config = {
            'site_name': whitelabel[0].site_name,
            'academy_link': whitelabel[0].academy_link,
            'browser_icon': whitelabel[0].browser_icon,
            'interface_icon': whitelabel[0].interface_icon,
            'interface_logo': whitelabel[0].interface_logo,
            'report_logo': whitelabel[0].report_logo
            }

     return config


