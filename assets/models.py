# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.forms.models import model_to_dict
from django.conf import settings

from events.models import Event
from common.utils.encoding import json_serial

import datetime
import os
import json

######## Rule Automation test - Made By BILL#######

from rules.models import Rule
import uuid
import hashlib


ASSET_TYPES = (
    ('ip', 'ip'),
    ('ip-range', 'ip-range'),       # 192.168.1.0-256
    ('ip-subnet', 'ip-subnet'),     # 192.168.1.0/24
    ('fqdn', 'fqdn'),
    ('domain', 'domain'),
    ('url', 'url'),
    ('keyword', 'keyword'),
    ('person', 'person'),
    ('organisation', 'organisation'),
    ('path', 'path'),
    ('application', 'application'),
)

ASSET_CRITICITIES = (
    ('low', 'low'),
    ('medium', 'medium'),
    ('high', 'high'),
)

TLP_COLORS = (
    ('red', 'red'),
    ('amber', 'amber'),
    ('green', 'green'),
    ('white', 'white'),
)


class AssetCategory(models.Model):
    parent   = models.ForeignKey('self', null=True, blank=None, default=None, related_name='children', on_delete=models.CASCADE)#, db_constraint=False)
    value    = models.CharField(max_length=512)  #256 - 512
    comments = models.CharField(max_length=512, null=True, blank=None, default="n/a")  #256 - 512

    class Meta:
        abstract = False
        db_table = 'asset_categories'
        verbose_name_plural = 'Categorias de Ativos'

    def __str__(self):
        return "{}".format(self.value)

    def get_root(self):
        if self.parent is None:
            return self
        r = None
        for p in AssetCategory.objects.filter(children=self):
            _p = p.get_root()
            if _p.parent is None:
                r = _p
        return r

    def get_all_parents(self):
        # todo: optimize with filter on p.parent only
        r = []
        if not self.parent:
            return None  # root
        r.append(self.parent)

        for p in AssetCategory.objects.filter(children=self):
            _r = p.get_all_parents()
            if _r:
                r.extend(_r)
        return r

    def get_siblings(self, include_self=False):
        if include_self:
            return AssetCategory.objects.filter(parent=self.parent)
        return AssetCategory.objects.filter(parent=self.parent).exclude(id=self.id)

    def get_children(self, include_self=False):
        r = []
        if include_self:
            r.append(self)
        for c in AssetCategory.objects.filter(parent=self):
            _r = c.get_children(include_self=True)
            if 0 < len(_r):
                r.extend(_r)
        return r

    def is_child_node(self):
        # has parent
        return self.parent is not None

    def is_leaf_node(self):
        # no children
        return self.children.count() == 0

    def is_root_node(self):
        # no parent
        return self.parent is None

    def add_child(self, value, comments=None):
        return AssetCategory.objects.create(parent=self, value=value, comments=comments)

    def delete(self, *args, **kwargs):
        self.get_children().delete()
        super(AssetCategory, self).delete(args, kwargs)

    # def show_children(self, level=0):
    #     r = "-"*level +" {}\n".format(self.value)
    #     for c in AssetCategory.objects.filter(parent=self):
    #         r = r + c.show_children(level=level+1)
    #     return r
    def show_children(self, level=0):
        r = []
        r.append((self.id, "-"*level + "{}\n".format(self.value)))
        for c in AssetCategory.objects.filter(parent=self).order_by('value'):
            r.extend(c.show_children(level=level+1))
        return r
    
    def to_dict(self):
        data = model_to_dict(self)
        if self.parent:
            data['parent'] = self.parent.id
        else:
            data['parent'] = None
        return data


@receiver(post_save, sender=AssetCategory)
def assetcat_create_update_log(sender, **kwargs):
    if kwargs['created']:
        Event.objects.create(message="[AssetCategory] Nova categoria de ativo criada (id={}): {}".format(kwargs['instance'].id, kwargs['instance']),
            type="CREATE", severity="DEBUG")
    else:
        Event.objects.create(message="[AssetCategory] Categoria de ativo '{}' modificada (id={})".format(kwargs['instance'], kwargs['instance'].id),
            type="UPDATE", severity="DEBUG")


@receiver(post_delete, sender=AssetCategory)
def assetcat_delete_log(sender, **kwargs):
    Event.objects.create(message="[AssetCategory] Categoria de ativo '{}' excluida (id={})".format(kwargs['instance'], kwargs['instance'].id),
        type="DELETE", severity="DEBUG")




# Modificacao risco quantitativo - "financeiro"
class Asset(models.Model):
    """Class definition of Asset."""

    value       	= models.CharField(max_length=512, unique=True, null=False) # 256 - 512
    name        	= models.CharField(max_length=512) #256 - 512
    type        	= models.CharField(choices=ASSET_TYPES, default='ip', max_length=15)  # ipv4, ipv6, domain, fqdn, url
    criticity   	= models.CharField(choices=ASSET_CRITICITIES, default='low', max_length=10)  # low, medium, high
    financeiro          = models.DecimalField(decimal_places=2, max_digits=11, null=True, blank=True)
#    financeiro          = MoneyField(decimal_places=2, max_digits=11, null=True, blank=True, validators=[ MinMoneyValidator(10), MaxMoneyValidator(1500),MinMoneyValidator(Money(500, 'BRL')), MaxMoneyValidator(Money(900, 'BRL')), MinMoneyValidator({'USD': 100, 'BRL': 50}), MaxMoneyValidator({'USD': 1000, 'BRL': 500}),])
    risk_level  	= JSONField(default=dict({"info": 0, "low": 0, "medium": 0, "high": 0, "critical": 0, "total": 0, "grade": "-"}))
    owner       	= models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    description 	= models.CharField(max_length=512, null=True, blank=True)  #256 - 512
    status      	= models.CharField(max_length=30, null=True, blank=True, default="new")
    categories  	= models.ManyToManyField(AssetCategory)
    created_at 		= models.DateTimeField(default=timezone.now)
    updated_at  	= models.DateTimeField(default=timezone.now)


    class Meta:
        """Metadata: DB name."""
        db_table = 'assets'

    def __str__(self):
        """Return Stringified class summary."""

        return "{}".format(self.value)

    def to_dict(self):
        """Return JSONified class summary."""
        data = model_to_dict(self, exclude=["categories"])
        data.update({"categories": [model_to_dict(c, fields=["value", "id"]) for c in self.categories.all()]})
        return json.loads(json.dumps(data, default=json_serial))

    def save(self, *args, **kwargs):
        """Update the 'updated_at' field on each updates."""
        if not self._state.adding:
            self.updated_at = timezone.now()
        return super(Asset, self).save(*args, **kwargs)

    def evaluate_risk(self):
        criticity_factor = 0
        if self.criticity == "low":
            criticity_factor = 1
        elif self.criticity == "medium":
            criticity_factor = 5
        elif self.criticity == "high":
            criticity_factor = 10

        risk_data = {
            "info": 0,
            "low": 0,
            "medium": 0,
            "high": 0,
            "critical": 0,
            "new": 0,
            "confirmed": 0,
            "mitigated": 0,
            "asset_criticity_level": self.criticity,
            "asset_criticity_factor": criticity_factor
        }

        return risk_data

    def get_risk_grade(self, history=None):  # history= nb days before
        if history:
            self.calc_risk_grade(history=history)
        return str(self.risk_level['grade'])

    def calc_risk_grade(self, history=None, update_groups=False):
        risk_level = {
            "info": 0, "low": 0, "medium": 0, "high": 0, "critical": 0,
            "total": 0, "grade": "-", "new": 0, "mitigated": 0, "confirmed": 0}

        if not history:
            findings = self.finding_set.all()
        else:
            startdate = datetime.datetime.today()
            enddate = startdate - datetime.timedelta(days=history)
            findings = self.finding_set.filter(created_at__lte=enddate)

        for finding in findings:
            risk_level['total'] = risk_level.get('total', 0) + 1
            risk_level[finding.status] = risk_level.get(finding.status, 0) + 1
            risk_level[finding.severity] = risk_level.get(finding.severity, 0) + 1
        if risk_level['critical'] == 0 and risk_level['high'] == 0 and risk_level['medium'] == 0 and risk_level['low'] == 0 and risk_level['info'] == 0 and risk_level['total'] == 0:
            risk_level['grade'] = "-"
        elif risk_level['confirmed'] == 0 and risk_level['new'] == 0 and risk_level['mitigated'] == 0:
            risk_level['grade'] = "A"
        elif risk_level['critical'] == 0 and risk_level['high'] == 0 and risk_level['medium'] == 0 and risk_level['low'] == 0 and risk_level['info'] >= 1:
            risk_level['grade'] = "C"
        elif risk_level['critical'] == 0 and risk_level['high'] == 0 and risk_level['medium'] == 0 and risk_level['low'] == 0 and risk_level['info'] == 0:
            risk_level['grade'] = "-"
        elif risk_level['critical'] == 0 and risk_level['high'] == 0 and risk_level['medium'] == 0 and risk_level['low'] == 0:
            risk_level['grade'] = "A"
        elif risk_level['critical'] == 0 and risk_level['high'] == 0 and risk_level['medium'] <= 1 and risk_level['low'] <= 5:
            risk_level['grade'] = "B"
        elif risk_level['critical'] == 0 and risk_level['high'] == 0 and risk_level['medium'] <= 5:
            risk_level['grade'] = "C"
        elif risk_level['critical'] == 0 and risk_level['high'] <= 1 and risk_level['medium'] <= 5:
            risk_level['grade'] = "D"
        elif risk_level['critical'] == 0 and risk_level['high'] <= 3:
            risk_level['grade'] = "E"
        elif risk_level['critical'] >= 1 or risk_level['high'] > 3:
            risk_level['grade'] = "F"
        else:
            risk_level['grade'] = "n/a"

        if not history:
            self.risk_level = risk_level
            self.save()

        # Update relative asset groups
        if update_groups:
            for ag in self.assetgroup_set.all():
                ag.calc_risk_grade()

        return risk_level

    def get_risk_score(self, history=None, force_calc=False):
        if force_calc:
            self.calc_risk_grade()
        risk_score = 0
        if self.risk_level['grade'] == "A":
            risk_score = 100
        elif self.risk_level['grade'] == "B":
            risk_score = 200
        elif self.risk_level['grade'] == "C":
            risk_score = 300
        elif self.risk_level['grade'] == "D":
            risk_score = 400
        elif self.risk_level['grade'] == "E":
            risk_score = 500
        elif self.risk_level['grade'] == "F":
            risk_score = 600
        else:
            risk_score = 0

        risk_score = risk_score + (self.risk_level['low'] * 1)
        risk_score = risk_score + (self.risk_level['medium'] * 3)
        risk_score = risk_score + (self.risk_level['high'] * 10)

        return risk_score
    
    

######################  Automate  Rule  Asset - By BILL #########################

    def evaluate_alert_rules(self, trigger='all'):
        if trigger == "all":
            rules = Rule.objects.filter(enabled=True, scope='asset')
        else:
            rules = Rule.objects.filter(enabled=True, scope='asset', trigger=trigger)
        nb_matches = 0
        for rule in rules:
            kwargs = {
                "id": self.id,
                rule.scope_attr+next(iter(rule.condition)): rule.condition.itervalues().next()
            }
            if Asset.objects.filter(**kwargs):
                #print "rule '{}' matches".format(rule.title)
                nb_matches += 1
                rule.notify(message="[Asset={}] {}".format(self.asset.value, self.asset.criticity, self.title), asset=self.asset, description=self.description)
        return nb_matches



@receiver(post_save, sender=Asset)
def asset_create_update_log(sender, **kwargs):
    if kwargs['created']:
        Event.objects.create(message="[Asset] Novo ativo criado (id={}): {}".format(kwargs['instance'].id, kwargs['instance']),
                             type="CREATE", severity="DEBUG")
    else:
        Event.objects.create(message="[Asset] Ativo '{}' modificado (id={})".format(kwargs['instance'], kwargs['instance'].id),
                             type="UPDATE", severity="DEBUG")


@receiver(post_delete, sender=Asset)
def asset_delete_log(sender, **kwargs):
    Event.objects.create(message="[Asset] Ativo '{}' excluido (id={})".format(kwargs['instance'], kwargs['instance'].id),
                 type="DELETE", severity="DEBUG")


class AssetGroup(models.Model):
    assets      = models.ManyToManyField(Asset)
    name        = models.CharField(max_length=512, unique=True) #256 - 512
    criticity   = models.CharField(choices=ASSET_CRITICITIES, default='None', max_length=10)
    risk_level  = JSONField(default=dict({"info": 0, "low": 0, "medium": 0, "high": 0, "total": 0, "grade": "-"}))
    owner       = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    description = models.CharField(max_length=512, null=True, blank=True) #256 - 512
    status      = models.CharField(max_length=30, null=True, blank=True)
    categories  = models.ManyToManyField(AssetCategory)
    created_at  = models.DateTimeField(default=timezone.now)
    updated_at  = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'asset_groups'

    def __str__(self):
        return "{}/{}".format(self.id, self.name)

    def save(self, *args, **kwargs):
        # update the 'updated_at' entry on each update except on creation
        if not self._state.adding:
            self.updated_at = timezone.now()
        return super(AssetGroup, self).save(*args, **kwargs)

    def get_asset_names(self):
        return ", ".join([asset.value for asset in self.assets.all()])

    def evaluate_risk(self):
        criticity_factor = 0
        if self.criticity == "low":
            criticity_factor = 1
        if self.criticity == "medium":
            criticity_factor = 5
        if self.criticity == "high":
            criticity_factor = 10

        # Todo: update each asset
        return None

    def get_risk_grade(self, history=None):
        if history:  # history= nb days before
            self.calc_risk_grade(history=history)
        return str(self.risk_level['grade'])

    def calc_risk_grade(self, history=None):
        risk_level = {
            "info": 0, "low": 0, "medium": 0, "high": 0,
            "total": 0, "grade": "-"}

        findings = []
        if not history:
            for a in self.assets.all():
                for f in a.finding_set.all():
                    findings.append(f)
        else:
            startdate = datetime.datetime.today()
            enddate = startdate - datetime.timedelta(days=history)
            for a in self.assets.all():
                for f in a.finding_set.filter(created_at__lte=enddate):
                    findings.append(f)

        for finding in findings:
            risk_level['total'] = risk_level.get('total', 0) + 1
            risk_level[finding.severity] = risk_level.get(finding.severity, 0) + 1

        if risk_level['high'] == 0 and risk_level['medium'] == 0 and risk_level['low'] == 0 and risk_level['info'] == 0:
            risk_level['grade'] = "-"
        if risk_level['high'] == 0 and risk_level['medium'] == 0 and risk_level['low'] == 0:
            risk_level['grade'] = "A"
        elif risk_level['high'] == 0 and risk_level['medium'] <= 1 and risk_level['low'] <= 5:
            risk_level['grade'] = "B"
        elif risk_level['high'] == 0 and risk_level['medium'] <= 5:
            risk_level['grade'] = "C"
        elif risk_level['high'] <= 1 and risk_level['medium'] <= 5:
            risk_level['grade'] = "D"
        elif risk_level['high'] <= 3:
            risk_level['grade'] = "E"
        elif risk_level['high'] > 3:
            risk_level['grade'] = "F"
        else:
            risk_level['grade'] = "n/a"

        if not history:
            self.risk_level = risk_level
            self.save()
        return risk_level

    def get_risk_score(self, history=None, force_calc=False):
        if force_calc:
            self.calc_risk_grade()
        risk_score = 0
        if self.risk_level['grade'] == "A":
            risk_score = 100
        elif self.risk_level['grade'] == "B":
            risk_score = 200
        elif self.risk_level['grade'] == "C":
            risk_score = 300
        elif self.risk_level['grade'] == "D":
            risk_score = 400
        elif self.risk_level['grade'] == "E":
            risk_score = 500
        elif self.risk_level['grade'] == "F":
            risk_score = 600
        else:
            risk_score = 0

        risk_score = risk_score + (self.risk_level['low'] * 1)
        risk_score = risk_score + (self.risk_level['medium'] * 3)
        risk_score = risk_score + (self.risk_level['high'] * 10)

        return risk_score
    
    def to_dict(self):
        data = model_to_dict(self, exclude=["assets", "categories"])
        data.update({
            "assets": [model_to_dict(asset, fields=["value", "id"]) for asset in self.assets.all()],
            "categories": [model_to_dict(category, fields=["value", "id"]) for category in self.categories.all()]
        })
        return json.loads(json.dumps(data, default=json_serial))
        


@receiver(post_save, sender=AssetGroup)
def assetgroup_create_update_log(sender, **kwargs):
    if kwargs['created']:
        Event.objects.create(message="[AssetGroup] Novo Grupo de Ativo criado (id={}): {}".format(kwargs['instance'].id, kwargs['instance']),
                             type="CREATE", severity="DEBUG")
    else:
        Event.objects.create(message="[AssetGroup] Grupo de Ativo '{}' modificado (id={})".format(kwargs['instance'], kwargs['instance'].id),
                             type="UPDATE", severity="DEBUG")


@receiver(post_delete, sender=AssetGroup)
def assetgroup_delete_log(sender, **kwargs):
    Event.objects.create(message="[AssetGroup] Grupo de Ativo '{}' Excluido (id={})".format(kwargs['instance'], kwargs['instance'].id),
                 type="DELETE", severity="DEBUG")


class AssetOwnerContact(models.Model):
    name       = models.CharField(max_length=512) # 256 - 512
    department = models.CharField(max_length=256, null=True, blank=True)
    title      = models.CharField(max_length=256, null=True, blank=True)
    email      = models.EmailField(null=True, blank=True)
    phone      = models.CharField(max_length=20, null=True, blank=True)
    address    = models.CharField(max_length=256, null=True, blank=True)
    url        = models.URLField(null=True, blank=True)
    comments   = models.CharField(max_length=256, null=True, blank=True)
    owner      = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'asset_owner_contacts'

    def __str__(self):
        return "{}/{}".format(self.id, self.name)

    def save(self, *args, **kwargs):
        if not self._state.adding:
            self.updated_at = timezone.now()
        return super(AssetOwnerContact, self).save(*args, **kwargs)


@receiver(post_save, sender=AssetOwnerContact)
def assetownercontact_create_update_log(sender, **kwargs):
    if kwargs['created']:
        Event.objects.create(message="[AssetOwnerContact] Novo contato do proprietario criado (id={}): {}".format(kwargs['instance'].id, kwargs['instance']),
                             type="CREATE", severity="DEBUG")
    else:
        Event.objects.create(message="[AssetOwnerContact] Contato do proprietario de ativo '{}' modificado (id={})".format(kwargs['instance'], kwargs['instance'].id),
                             type="UPDATE", severity="DEBUG")

@receiver(post_delete, sender=AssetOwnerContact)
def assetownercontact_delete_log(sender, **kwargs):
    Event.objects.create(message="[AssetOwnerContact] Contato do proprietario do ativo '{}' excluido (id={})".format(kwargs['instance'], kwargs['instance'].id),
                 type="DELETE", severity="DEBUG")


class AssetOwnerDocument(models.Model):
    file       = models.FileField(null=True, blank=True)
    doctitle   = models.CharField(max_length=256, null=True, blank=True)
    filename   = models.CharField(max_length=256, null=True, blank=True)
    filepath   = models.CharField(max_length=256, null=True, blank=True)
    tlp_color  = models.CharField(choices=TLP_COLORS, default='red', max_length=10)
    comments   = models.CharField(max_length=256, null=True, blank=True)
    owner      = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'asset_owner_docs'

    def __str__(self):
        return "{}/{}".format(self.id, self.doctitle)

    def save(self, *args, **kwargs):
        if not self._state.adding:
            self.updated_at = timezone.now()
        return super(AssetOwnerDocument, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Delete related documents
        if self.filepath is not None and os.path.exists(self.filepath):
            os.remove(self.filepath)
        return super(AssetOwnerDocument, self).delete(*args, **kwargs)


@receiver(post_save, sender=AssetOwnerDocument)
def assetownerdoc_create_update_log(sender, **kwargs):
    if kwargs['created']:
        Event.objects.create(message="[AssetOwnerDocument] Novo documento do Ativo postado, salvo e indexado   (id={}): {}".format(kwargs['instance'].id, kwargs['instance']),
                             type="CREATE", severity="DEBUG")
    else:
        Event.objects.create(message="[AssetOwnerDocument] Documento do Ativo '{}' modificado (id={})".format(kwargs['instance'], kwargs['instance'].id),
                             type="UPDATE", severity="DEBUG")

@receiver(post_delete, sender=AssetOwnerDocument)
def assetownerdoc_delete_log(sender, **kwargs):
    Event.objects.create(message="[AssetOwnerDocument] Documento do Ativo '{}' excluido (id={})".format(kwargs['instance'], kwargs['instance'].id),
                 type="DELETE", severity="DEBUG")


class AssetOwner(models.Model):
    assets     = models.ManyToManyField(Asset)
    contacts   = models.ManyToManyField(AssetOwnerContact)
    documents  = models.ManyToManyField(AssetOwnerDocument)
    owner      = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    name       = models.CharField(max_length=256)
    url        = models.URLField(null=True, blank=True)
    comments   = models.CharField(max_length=256, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'asset_owners'

    def __str__(self):
        return "{}/{}".format(self.id, self.name)

    def save(self, *args, **kwargs):
        if not self._state.adding:
            self.updated_at = timezone.now()
        return super(AssetOwner, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):

        # Todo: change this !!

        # Delete related documents
        for doc in self.documents.all():
            try:
                doc.delete()
            except AssetOwnerDocument.DoesNotExist:
                pass
        # Delete related contacts
        for contact in self.contacts.all():
            try:
                contact.delete()
            except AssetOwnerContact.DoesNotExist:
                pass

        return super(AssetOwner, self).delete(*args, **kwargs)
    
    def to_dict(self):
        data = model_to_dict(self, exclude=["assets", "contacts", "documents"])
        data.update({
            "assets": [model_to_dict(asset, fields=["value", "id"]) for asset in self.assets.all()],
            "contacts": [model_to_dict(contact, fields=["name", "id"]) for contact in self.contacts.all()],
            "documents": [model_to_dict(document, fields=["doctitle", "id"]) for document in self.documents.all()]
        })
        return json.loads(json.dumps(data, default=json_serial))



@receiver(post_save, sender=AssetOwner)
def assetowner_create_update_log(sender, **kwargs):
    if kwargs['created']:
        Event.objects.create(message="[AssetOwner] Novo Proprietario do Ativo criado (id={}): {}".format(kwargs['instance'].id, kwargs['instance']),
                             type="CREATE", severity="DEBUG")
    else:
        Event.objects.create(message="[AssetOwner] Proprietario do Ativo '{}' modificado (id={})".format(kwargs['instance'], kwargs['instance'].id),
                             type="UPDATE", severity="DEBUG")


@receiver(post_delete, sender=AssetOwner)
def assetowner_delete_log(sender, **kwargs):
    Event.objects.create(message="[AssetOwner] Proprietario do Ativo '{}' excluido (id={})".format(kwargs['instance'], kwargs['instance'].id),
                 type="DELETE", severity="DEBUG")


ASSET_INVESTIGATION_LINKS = [
    {
        "name": "Alienvault OTX",
        "link": "https://otx.alienvault.com/indicator/ip/%asset%",
        "datatypes": ["ip"]
    },
    {
        "name": "Alienvault OTX",
        "link": "https://otx.alienvault.com/indicator/domain/%asset%",
        "datatypes": ["domain"]
    },
   # {
   #     "name": "Alexa",
   #     "link": "https://www.alexa.com/siteinfo/%asset%",
   #     "datatypes": ["domain"]
   # },
    {
        "name": "Censys (IP)",
        "link": "https://censys.io/ipv4/%asset%",
        "datatypes": ["ip"]
    },
    {
        "name": "Censys (Domain)",
        "link": "https://censys.io/domain/%asset%",
        "datatypes": ["domain"]
    },
    {
        "name": "Censys (Certificates)",
        "link": "https://censys.io/certificates?q=parsed.names%3A%20%asset%",
        "datatypes": ["domain"]
    },
 #   {
 #       "name": "Cymon",
 #       "link": "https://cymon.io/domain/%asset%",
 #       "datatypes": ["domain"]
 #   },
 #   {
 #       "name": "Cymon",
 #       "link": "https://cymon.io/%asset%",
 #       "datatypes": ["ip"]
 #   },
 #   {
 #       "name": "DNSLytics",
 #       "link": "https://dnslytics.com/domain/%asset%",
 #       "datatypes": ["domain", "fqdn"]
 #   },
 #   {
 #       "name": "DNSLytics",
 #       "link": "https://dnslytics.com/ip/%asset%",
 #       "datatypes": ["ip"]
 #   },
 #   {
 #       "name": "HerdProtect",
 #       "link": "http://www.herdprotect.com/ip-address-%asset%.aspx",
 #       "datatypes": ["ip"]
 #   },
 #   {
 #       "name": "HerdProtect",
 #       "link": "http://www.herdprotect.com/domain-%asset%.aspx",
 #       "datatypes": ["domain"]
 #   },
 #   {
 #       "name": "Quttera",
 #       "link": "https://quttera.com/sitescan/%asset%",
 #       "datatypes": ["domain"]
 #   },
 #   {
 #       "name": "Sucuri",
 #       "link": "https://sitecheck.sucuri.net/results/%asset%",
 #       "datatypes": ["domain"]
 #   },
 #   {
 #       "name": "URLVoid",
 #       "link": "http://www.urlvoid.com/scan/%asset%",
 #       "datatypes": ["url"]
 #   },
 #   {
 #       "name": "Netcraft",
 #       "link": "https://toolbar.netcraft.com/site_report?url=%asset%",
 #       "datatypes": ["url", "ip"]
 #   },
 #   {
 #       "name": "Netcraft",
 #       "link": "https://searchdns.netcraft.com/?host=%asset%",
 #       "datatypes": ["domain"]
 #   },
 #   {
 #       "name": "VirusTotal",
 #       "link": "https://www.virustotal.com/en/domain/%asset%/information/",
 #       "datatypes": ["domain"]
 #   },
 #   {
 #       "name": "VirusTotal",
 #       "link": "https://www.virustotal.com/en/ip-address/%asset%/information/",
 #       "datatypes": ["ip"]
 #   },
 #   {
 #       "name": "VirusTotal",
 #       "link": "https://www.virustotal.com/en/url/submission/?force=1&url=%asset%",
 #       "datatypes": ["url"]
 #   },
 #   {
 #       "name": "Whois",
 #       "link": "http://whois.domaintools.com/%asset%",
 #       "datatypes": ["domain", "ip"]
 #   },
 #   {
 #       "name": "Security Headers",
 #       "link": "https://securityheaders.com/?q=%asset%&followRedirects=on",
 #       "datatypes": ["domain", "url"]
 #   },
 #   {
 #       "name": "Security Trails",
 #       "link": "https://securitytrails.com/domain/%asset%/dns",
 #       "datatypes": ["domain"]
 #   },
 #   {
 #       "name": "Security Trails",
 #       "link": "https://securitytrails.com/list/ip/%asset%",
 #       "datatypes": ["ip"]
 #   },
 #   {
 #       "name": "Shodan.io",
 #       "link": "https://www.shodan.io/host/%asset%",
 #       "datatypes": ["ip"]
 #   },
 #   {
 #       "name": "Shodan.io (Search)",
 #       "link": "https://www.shodan.io/search?query=%asset%",
 #       "datatypes": ["ip", "domain"]
 #   },
 #   {
 #       "name": "Talos Reputation (Cisco)",
 #       "link": "https://talosintelligence.com/reputation_center/lookup?search=%asset%",
 #       "datatypes": ["ip", "fqdn", "domain"]
 #   },
    {
        "name": "ThreatCrowd",
        "link": "https://www.threatcrowd.org/domain.php?domain=%asset%",
        "datatypes": ["domain"]
    },
   # {
   #     "name": "ThreatCrowd (API)",
   #     "link": "https://www.threatcrowd.org/searchApi/v2/domain/report/?domain=%asset%",
   #     "datatypes": ["domain"]
   # },
    {
        "name": "ThreatCrowd",
        "link": "https://www.threatcrowd.org/ip.php?ip=%asset%",
        "datatypes": ["ip"]
    },
 #   {
 #       "name": "ThreatCrowd (API)",
 #       "link": "https://www.threatcrowd.org/searchApi/v2/ip/report/?ip=%asset%",
 #       "datatypes": ["ip"]
 #   },
    {
        "name": "Threat Miner",
        "link": "https://www.threatminer.org/host.php?q=%asset%",
        "datatypes": ["ip"]
    },
    {
        "name": "Threat Miner",
        "link": "https://www.threatminer.org/domain.php?q=%asset%",
        "datatypes": ["domain"]
    },
    ]
