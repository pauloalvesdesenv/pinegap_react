# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os, sys
from whitelabels.models import Brand


def whitelabel_renderer(request):
     whitelabel = Brand.objects.all().order_by('id')

     if whitelabel.count() <= 0:

        config = {
            'site_name': 'Pinegap Platform',
            'academy_link': 'https://conhecimento.pinegap.io/',
            'browser_icon': 'media/default_logos/dist/img/favicon1.ico',
            'interface_icon': 'media/default_logos/dist/img/logo-pinegap-mini.png',
            'interface_logo': 'media/default_logos/dist/img/logo-pinegap.png',
            'report_logo': 'media/default_logos/report/img/logo.png'
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



