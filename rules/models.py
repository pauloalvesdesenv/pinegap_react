# -*- coding: utf-8 -*-

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from events.models import Event
from settings.models import Setting
from django_celery_beat.models import PeriodicTask

import json
import requests
import uuid
from thehive4py.api import TheHiveApi
from thehive4py.models import Alert, AlertArtifact

RULE_SCOPES = (
    #('asset', 'Ativo'),
    ('finding', 'Ocorrência'),
    #('scan', 'Scan'),
)

RULE_SCOPE_ATTRIBUTES = {
    "asset": {
        # 'value':        {"type": "numeric"},
        'value':         {"type": "text"},
        'name':          {"type": "text"},
        'type':          {"type": "list", "values": ['ip', 'domain', 'url']},
        'description':   {"type": "text"},
        'criticity':     {"type": "list", "values": ['low', 'medium', 'high']}
        },
    "finding": {
        'title':       {"type": "text"},
        'description':  {"type": "text"},
        'type':        {"type": "text"},
        'hash':        {"type": "text"},
        'solution':    {"type": "text"},
        'severity':    {"type": "list", "values": ['info', 'low', 'medium', 'high', 'critical']},
        'status':      {"type": "list", "values": ['new', 'ack', 'mitigated', 'confirmed', 'patched', 'closed', 'false-positive']},
        # 'tags':         {"type": "in_list"},
        },
    # "scan": {
    #     'status': {"type": "text"},
    #     },
}

RULE_TARGETS = (
    ('event',   'Gerar Evento'),
    ('logfile', 'Log em Arquivo'),
    ('email',   'Enviar e-mail'),
#    ('thehive', 'ECO-FIR'),
    ('splunk',  'Log Splunk'),
    ('slack',   'Msg Slack'),
    ('hostsgreen',   'Hosts Green'),
)

RULE_TRIGGERS = (
    ('ondemand', 'Pontual'),
    ('auto', 'Recorrente'),  # frequency ?
)

RULE_CONDITIONS = {
    'text': {
        "__iexact":      "Exatamente",
        "__icontains":   "Contêm",
        "__istartswith": "Começa com",
        "__iendswith":   "Termina com",
    },
    'numeric': {
        "__gt":  ">",
        "__gte": "> ou =",
        "__lt":  "<",
        "__lte": "< ou =",
    },
    'list': None,  # see values
}

RULE_SEVERITIES = (
    ('low',    'Baixa'),
    ('medium', 'Média'),
    ('high',   'Alta'),
)


class Rule(models.Model):
    title            = models.CharField(max_length=256)
    comments         = models.CharField(max_length=256, default='n/a')
    scope            = models.CharField(choices=RULE_SCOPES, default='finding', max_length=10)
    scope_attr       = models.CharField(max_length=20, null=True, blank=True)
    condition        = JSONField(null=True, blank=True)
    target           = models.CharField(choices=RULE_TARGETS, default='event', max_length=10)
    severity         = models.CharField(choices=RULE_SEVERITIES, default='low', max_length=10)
    trigger          = models.CharField(choices=RULE_TRIGGERS, max_length=10)
    trigger_attr     = models.CharField(max_length=20, null=True, blank=True)
    summary          = JSONField(null=True, blank=True)
    periodic_task    = models.ForeignKey(PeriodicTask, null=True, blank=True, on_delete=models.CASCADE)
    enabled          = models.BooleanField(default=False)
    nb_matches       = models.IntegerField(default=0)
    owner            = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at       = models.DateTimeField(default=timezone.now)
    updated_at       = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'rules'

    def __str__(self):
        return "{}/{}".format(self.id, self.title)

    def save(self, *args, **kwargs):
        if not self._state.adding:
            self.updated_at = timezone.now()
        return super(Rule, self).save(*args, **kwargs)

    def notify(self, message="", asset=None, description=""):
        if self.target == 'email':
            send_email_message(self, message, description)
        elif self.target == 'slack':                # Correção Slack By Bill
            send_slack_message(self, message)	    # Correção Slack By Bill
        elif self.target == 'hostsgreen':           # Add Hostsgreen By Bill
            send_hostsgreen_message(self, message)  # Add Hostsgreen By Bill
        elif self.target == 'thehive':
            send_thehive_message(self, message, asset, description)
        elif self.target == 'event':
            Event.objects.create(
                message="[Alert][Rule={}]{}".format(self.title, message),
                type="ALERT", severity="INFO")

        self.nb_matches += 1
        print (self.nb_matches)
        self.save()


@receiver(post_save, sender=Rule)
def rule_create_update_log(sender, **kwargs):
    if kwargs['created']:
        Event.objects.create(message="[Rule] Nova regra criada (id={}): {}".format(kwargs['instance'].id, kwargs['instance']),
                             type="CREATE", severity="DEBUG")
    else:
        Event.objects.create(message="[Rule] Rule '{}' modificada (id={})".format(kwargs['instance'], kwargs['instance'].id),
                             type="UPDATE", severity="DEBUG")


@receiver(post_delete, sender=Rule)
def rule_delete_log(sender, **kwargs):
    Event.objects.create(message="[Rule] Regra '{}' excluida (id={})".format(kwargs['instance'], kwargs['instance'].id),
                 type="DELETE", severity="DEBUG")


def send_email_message(rule, message, description):
    contact_mail = Setting.objects.get(key="alerts.endpoint.email").value
    send_mail(
        'PineGap Novo alerta de Vulnerabilidade: ',
        'Encontramos estas vulnerabilidades aqui : '+message,
        'alerts@pinegap.io',
        [contact_mail],
        fail_silently=False,
    )

def send_slack_message(rule, message):
    Event.objects.create(message="[Regra] Rule '{}' Slack alert creation (message={})".format(rule, message)[:250], type="CREATE", severity="DEBUG")
    slack_url = Setting.objects.get(key="alerts.endpoint.slack.webhook")
    alert_message = "[Alerta][Regra={}]{}".format(rule.title, message)
    try:
        slack_channel = Setting.objects.get(key="alerts.endpoint.slack.channel")
    except:
        slack_channel = None
    alert_message = "[Alerta][Regra={}]{}".format(rule.title, message)
    data_payload = {'text': alert_message}
    if slack_channel:
        data_payload["channel"] = slack_channel.value
    try:
        requests.post(
            slack_url.value,
#            data=json.dumps({'text': alert_message}),
	    data=json.dumps(data_payload),
            headers={'content-type': 'application/json'})
#    except Exception:
#        Event.objects.create(message="[Rule] Send slack message failed (id={})".format(rule.id),
#                     type="ERROR", severity="ERROR", description=alert_message)
    except Exception as e:
        Event.objects.create(message="err:{} [Rule] Send slack message failed (id={})".format(e, rule.id)[:250],
                     type="ERROR", severity="ERROR", description=alert_message)

def send_hostsgreen_message(rule, message):
    event = Event.objects.create(message="[Regra] Regra '{}' Hosts Green Alert (message={})".format(rule, message)[:250], type="CREATE", severity="DEBUG")
    hostsgreen_url = Setting.objects.get(key="alerts.endpoint.hostsgreen.webhook")
    try:
        hostsgreen_channel = Setting.objects.get(key="alerts.endpoint.hostsgreen.channel")
    except:
        hostsgreen_channel = None
    alert_message = "[Alerta][Regra={}]{}".format(rule.title, message)
    data_payload = {'text': alert_message}
    if hostsgreen_channel:
        data_payload["channel"] = hostsgreen_channel.value
    try:
        requests.post(
            hostsgreen_url.value,
#           data=json.dumps({'text': alert_message}),
            data=json.dumps(data_payload),
            headers={'content-type': 'application/json'})
    except Exception as e:
        Event.objects.create(message="err:{} [Rule] API falhou ao enviar mensagens ao Hosts Green (id={})".format(e, rule.id)[:250],
                     type="ERROR", severity="ERROR", description=alert_message)

def send_thehive_message(rule, message, asset, description):
    print("send_thehive_message:", rule, message, asset, description)
    thehive_url = Setting.objects.get(key="alerts.endpoint.thehive.url")
    thehive_apikey = Setting.objects.get(key="alerts.endpoint.thehive.apikey")
    alert_message = "[Alert][Rule={}]{}".format(rule.title, message)

    api = TheHiveApi(thehive_url.value, thehive_apikey.value)
    sourceRef = str(uuid.uuid4())[0:6]
    rule_severity = 0
    if rule.severity == "Low":
        rule_severity = 1
    elif rule.severity == "Medium":
        rule_severity = 2
    elif rule.severity == "High":
        rule_severity = 3

    tlp = 0
    if asset.criticity == "low":
        tlp = 1
    elif asset.criticity == "medium":
        tlp = 2
    elif asset.criticity == "high":
        tlp = 3

    if asset:
        artifacts = [AlertArtifact(dataType=asset.type, data=asset.value)]
        try:
            alert = Alert(
                        title=alert_message,
                        tlp=tlp,
                        severity=rule_severity,
                        tags=['src:Pinegap'],
                        description=description,
                        type='external',
                        source='pinegap',
                        sourceRef=sourceRef,
                        artifacts=artifacts)

            response = api.create_alert(alert)

            if response.status_code == 201:
                alert_id = response.json()['id']
                # todo: track theHive alerts
            else:
                Event.objects.create(
                    message="[Rule][send_thehive_message()] Unable to send "
                    "alert to TheHive with message ='{}'".format(message),
                    type="ERROR", severity="ERROR"
                )
        except Exception:
            Event.objects.create(
                message="[Rule][send_thehive_message()] Unable to send alert "
                "to TheHive with message ='{}'".format(message),
                type="ERROR", severity="ERROR")
