# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import Scan, ScanCampaign, ScanDefinition

admin.site.register(Scan)
admin.site.register(ScanCampaign)
admin.site.register(ScanDefinition)
