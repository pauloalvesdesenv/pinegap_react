# -*- coding: utf-8 -*-

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.forms.models import model_to_dict

from events.models import Event
from assets.models import Asset
from scans.models import Scan
from rules.models import Rule
from engines.models import EnginePolicyScope
from common.utils.encoding import json_serial
from settings.models import Setting

import json
import uuid
import hashlib


FINDING_SEVERITIES = (
    ('info', 'Desconhecida'),
    ('low', 'Baixa'),
    ('medium', 'Média'),
    ('high', 'Alta'),
    ('critical', 'Crítica')
)

FINDING_STATUS = (
    ('new', 'Nova'),
    ('ack', 'Ignorada'),
    ('mitigated', 'Mitigada'),
    ('confirmed', 'Confirmada'),
    ('patched', 'Corrigida'),
    ('closed', 'Encerrada'),
    ('false-positive', 'Falso-Positivo')
)


class RawFinding(models.Model):
    # asset       = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='raw_findings')
    asset       = models.ForeignKey(Asset, on_delete=models.CASCADE)
    asset_name  = models.CharField(max_length=256)
    task_id     = models.UUIDField(default=uuid.uuid4, editable=True)
    # scan        = models.ForeignKey(Scan, on_delete=models.CASCADE, related_name='raw_findings')
    scan        = models.ForeignKey(Scan, on_delete=models.CASCADE)
    owner       = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    title       = models.CharField(max_length=256)
    type        = models.CharField(max_length=50)
    hash        = models.CharField(max_length=256)
    confidence  = models.CharField(max_length=10)
    severity    = models.CharField(choices=FINDING_SEVERITIES, default='info', max_length=10)
    severity_num= models.IntegerField(default=1, blank=True, null=True)
    scopes      = models.ManyToManyField(EnginePolicyScope, blank=True)
    description = models.TextField(max_length=10240)
    solution    = models.TextField(max_length=5120, null=True, blank=True)
    raw_data    = JSONField(null=True, blank=True)
    risk_info   = JSONField(null=True, blank=True)
    vuln_refs   = JSONField(null=True, blank=True)
    links       = JSONField(null=True, blank=True)
    tags        = JSONField(null=True, blank=True)
    status      = models.CharField(choices=FINDING_STATUS, max_length=16)
    engine_type = models.CharField(max_length=20)
    found_at    = models.DateTimeField(null=True, blank=True)
    checked_at  = models.DateTimeField(null=True, blank=True)
    comments    = models.TextField(max_length=5120, default="N/A", null=True, blank=True)
    created_at  = models.DateTimeField(default=timezone.now)
    updated_at  = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'raw_findings'

    def __str__(self):
        return "{}/{}/{}".format(self.id, self.asset.value, self.title)

    def get_risk(self):
        return (self.severity, self.confidence)

    def save(self, *args, **kwargs):
        self.hash = hashlib.sha1(str(self.asset_name)+str(self.title)).hexdigest()
        if self.severity == "info":
            self.severity_num = 1
        elif self.severity == "low":
            self.severity_num = 2
        elif self.severity == "medium":
            self.severity_num = 3
        elif self.severity == "high":
            self.severity_num = 4
        else:
            self.severity_num = 0
        # update the 'updated_at' entry on each update except on creation
        if not self._state.adding:
            self.updated_at = timezone.now()
        return super(RawFinding, self).save(*args, **kwargs)

    def evaluate_alert_rules(self, trigger='all'):
        if trigger == "all":
            rules = Rule.objects.filter(enabled=True, scope='finding')
        else:
            rules = Rule.objects.filter(enabled=True, scope='finding', trigger=trigger)
        nb_matches = 0
        for rule in rules:
            kwargs = {
                "id": self.id,
                rule.scope_attr+next(iter(rule.condition)): rule.condition.itervalues().next()
            }
            if RawFinding.objects.filter(**kwargs):
                #print "rule '{}' matches".format(rule.title)
                nb_matches += 1
                rule.notify(message="[Asset={}] {}".format(self.asset.value, self.title), asset=self.asset)
        return nb_matches


@receiver(post_save, sender=RawFinding)
def rawfinding_create_update_log(sender, **kwargs):
    if kwargs['created']:
        Event.objects.create(message="[RawFinding] New raw finding created (id={}): {}".format(kwargs['instance'].id, kwargs['instance']),
                             type="CREATE", severity="DEBUG")
    else:
        Event.objects.create(message="[RawFinding] Raw finding '{}' modified (id={})".format(kwargs['instance'], kwargs['instance'].id),
                             type="UPDATE", severity="DEBUG")


@receiver(post_delete, sender=RawFinding)
def rawfinding_delete_log(sender, **kwargs):
    Event.objects.create(message="[RawFinding] Raw finding '{}' deleted (id={})".format(kwargs['instance'], kwargs['instance'].id),
                 type="DELETE", severity="DEBUG")


class Finding(models.Model):
    raw_finding = models.ForeignKey(RawFinding, models.SET_NULL, blank=True, null=True)
    # asset       = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='findings')
    asset       = models.ForeignKey(Asset, on_delete=models.CASCADE)
    asset_name  = models.CharField(max_length=256) #todo: delete this
    task_id     = models.UUIDField(default=uuid.uuid4, editable=True)
    scan        = models.ForeignKey(Scan, on_delete=models.CASCADE)
    owner       = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    title       = models.CharField(max_length=256, default='title')
    type        = models.CharField(max_length=50)
    hash        = models.CharField(max_length=256)
    confidence  = models.CharField(max_length=10)
    severity    = models.CharField(choices=FINDING_SEVERITIES, default='info', max_length=10)  # info, low, medium, high, critical
    severity_num= models.IntegerField(default=1, blank=True, null=True)  # info, low, medium, high, critical
    scopes      = models.ManyToManyField(EnginePolicyScope, blank=True)
    description = models.TextField(max_length=10240)
    solution    = models.TextField(max_length=5120, null=True, blank=True)
    raw_data    = JSONField(null=True, blank=True)
    risk_info   = JSONField(null=True, blank=True)
    vuln_refs   = JSONField(null=True, blank=True)
    links       = JSONField(null=True, blank=True)
    tags        = JSONField(null=True, blank=True)
    status      = models.CharField(choices=FINDING_STATUS, max_length=16, default='new')
    engine_type = models.CharField(max_length=20)
    found_at    = models.DateTimeField(default=timezone.now)
    comments    = models.TextField(max_length=5120, default="N/A", null=True, blank=True)
    checked_at  = models.DateTimeField(default=timezone.now)
    created_at  = models.DateTimeField(default=timezone.now)
    updated_at  = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'findings'

    def __str__(self):
        return "{}/{}".format(self.id, self.title)

    def to_dict(self):
        """Return JSONified class summary."""
        data = model_to_dict(self, exclude=["scopes"])
        data.update({"scopes": [model_to_dict(s, fields=["name", "id"]) for s in self.scopes.all()]})
        return json.loads(json.dumps(data, default=json_serial))

    def get_risk(self):
        return (self.severity, self.confidence)

    def save(self, *args, **kwargs):
        self.hash = hashlib.sha1(str(self.asset_name)+str(self.title)).hexdigest()
        if self.severity == "info":
            self.severity_num = 1
        elif self.severity == "low":
            self.severity_num = 2
        elif self.severity == "medium":
            self.severity_num = 3
        elif self.severity == "high":
            self.severity_num = 4
        else:
            self.severity_num = 0

        # update the 'updated_at' entry on each update except on creation
        if not self._state.adding:
            self.updated_at = timezone.now()
        return super(Finding, self).save(*args, **kwargs)
    
    def translate_severity(self):
        if self.severity == "info":
            return "Desconhecida"
        if self.severity == "low":
            return "Baixa"
        if self.severity == "medium":
            return "Média"
        if self.severity == "high":
            return "Alta"
        if self.severity == "critical":
            return "Crítica"

    def translate_status(self):
        if self.status == "new":
            return "Nova"
        if self.status == "ack":
            return "Ignorada"
        if self.status == "mitigated":
            return "Mitigada"
        if self.status == "confirmed":
            return "Confirmada"
        if self.status == "patched":
            return "Corrigida"
        if self.status == "closed":
            return "Encerrada"
        if self.status == "false-positive":
            return "Falso-Positivo"    

    def evaluate_alert_rules(self, trigger='all'):
        setting = Setting.objects.filter(key="url_setting")[0]
        url = "https://"+setting.value+"/findings/details/"+str(self.id)
        if trigger == "all":
            rules = Rule.objects.filter(enabled=True, scope='finding')
        else:
            rules = Rule.objects.filter(enabled=True, scope='finding', trigger=trigger)
        nb_matches = 0
        for rule in rules:
            kwargs = {
                "id": self.id,
                rule.scope_attr+next(iter(rule.condition)): rule.condition.itervalues().next()
            }
            if Finding.objects.filter(**kwargs):
                nb_matches += 1
                rule.notify(message="[Ativo={}][Status={}][Url={}][Tipo={}][Severidade={}] {}".format(self.asset.value, self.translate_status(), url, self.type, self.translate_severity(), self.title), asset=self.asset, description=self.description) 
        return nb_matches


@receiver(post_save, sender=Finding)
def finding_create_update_log(sender, **kwargs):
    if kwargs['created']:
        Event.objects.create(message="[Finding] New finding created (id={}): {}".format(kwargs['instance'].id, kwargs['instance']),
                             type="CREATE", severity="DEBUG")
    else:
        kwargs['instance'].asset.calc_risk_grade()
        Event.objects.create(message="[Finding] Finding '{}' modified (id={})".format(kwargs['instance'], kwargs['instance'].id),
                             type="UPDATE", severity="DEBUG")


@receiver(post_delete, sender=Finding)
def finding_delete_log(sender, **kwargs):
    asset = Asset.objects.get(id=kwargs['instance'].asset_id)
    asset.calc_risk_grade()

    Event.objects.create(message="[Finding] Finding '{}' deleted (id={})".format(kwargs['instance'], kwargs['instance'].id),
                 type="DELETE", severity="DEBUG")
