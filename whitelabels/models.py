from django.db import models
from django.utils import timezone
from django.core.files import File
import os
from django.core.urlresolvers import reverse


# WHITELABEL - DONE BY BILL



class Whitelabel(models.Model):
    site_name      = models.CharField(max_length=255, null=False, default='Pinegap Platform')
    academy_link   = models.CharField(max_length=255, null=False, default='conhecimento.pinegap.io')
    browser_icon   = models.FileField(null=False, upload_to='static/whitelabel/icon_browser/')
    interface_icon = models.FileField(null=False, upload_to='static/whitelabel/icon_interface/')
    interface_logo = models.FileField(null=False, upload_to='static/whitelabel/logo_interface/')
    report_logo    = models.FileField(null=False, upload_to='static/whitelabel/logo_report/')



    class Meta:
        db_table = 'whitelabels'
        managed = True

    def __str__(self):
        return  (self.id)

    def save(self):
        if self.academy_link[:4] == "www.":
            self.academy_link = self.academy_link.replace(self.academy_link[:4], '')
        elif self.academy_link[:7] == "http://":
            self.academy_link = self.academy_link.replace(self.academy_link[:7], '')
        elif self.academy_link[:8] == "https://":
            self.academy_link = self.academy_link.replace(self.academy_link[:8], '')
        super(Whitelabel, self).save()





class Brand(models.Model):
    id		   = models.CharField(max_length=255, null=False, primary_key=True)
    site_name      = models.CharField(max_length=255, null=False)
    academy_link   = models.CharField(max_length=255, null=False)
    browser_icon   = models.CharField(max_length=255, null=False)
    interface_icon = models.CharField(max_length=255, null=False)
    interface_logo = models.CharField(max_length=255, null=False)
    report_logo    = models.CharField(max_length=255, null=False)



    class Meta:
        db_table = 'whitelabels'
	managed = False

    def __str__(self):
        return  (self.id)

