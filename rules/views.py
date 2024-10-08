# -*- coding: utf-8 -*-
"""Views for alerting rules."""

from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from settings.models import Setting
from .models import Rule, RULE_SCOPES, RULE_SCOPE_ATTRIBUTES, RULE_TARGETS
from .models import RULE_TRIGGERS, RULE_CONDITIONS, RULE_SEVERITIES
import json
import requests

############## Implement Control Access of Url - By BILL #############
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404

######################################################################

def list_rules_api(request):
    """API: List alerting rules."""
    # rules = Rule.objects.all()

    return JsonResponse('todo')


def list_rules_view(request):
    """View: List alerting rules.

    **Context**

    ``Rule``
        An instance of :model:`rules.models.Rule`.

    **Template:**

    :template:`rules/templates/list-rules.html`
    """
    form_options = {
        "rule_scopes": RULE_SCOPES,
        "rule_scope_attributes": json.dumps(RULE_SCOPE_ATTRIBUTES),
        "rule_conditions": json.dumps(RULE_CONDITIONS),
        "rule_targets": RULE_TARGETS,
        "rule_triggers": RULE_TRIGGERS,
        "rule_severities": RULE_SEVERITIES,
    }
    rules_list = Rule.objects.all().order_by('-created_at')

    paginator = Paginator(rules_list, 80)
    page = request.GET.get('page')
    try:
        rules = paginator.page(page)
    except PageNotAnInteger:
        rules = paginator.page(1)
    except EmptyPage:
        rules = paginator.page(paginator.num_pages)
    return render(request, 'list-rules.html', {
        'rules': rules, 'form_options': form_options})




# Add Bloqueio de URL - By BILL
@user_passes_test(lambda u: u.groups.filter(name='visitante').count() == 0, login_url='/rules/deny/')
@user_passes_test(lambda u: u.groups.filter(name='analista').count() == 0,  login_url='/rules/deny/')
@user_passes_test(lambda u: u.groups.filter(name='dpo').count() == 0, login_url='/rules/deny/')
@csrf_exempt  # not secure
def delete_rules_api(request):
    """API: Delete alerting rules."""
    if not request.method == 'POST':
        return JsonResponse(
            {'status': 'error'}, json_dumps_params={'indent': 2}, status=403)

    rules_to_delete = json.loads(request.body)
    rule = get_object_or_404(Rule, id=rules_to_delete[0])
    rule.delete()
    messages.success(request, 'Regra excluida com sucesso!')

    return JsonResponse(
        {'status': 'success'},
        json_dumps_params={'indent': 2}
    )



# Add Bloqueio de URL - By BILL
@user_passes_test(lambda u: u.groups.filter(name='visitante').count() == 0, login_url='/rules/deny/')
@user_passes_test(lambda u: u.groups.filter(name='analista').count() == 0,  login_url='/rules/deny/')
@user_passes_test(lambda u: u.groups.filter(name='dpo').count() == 0, login_url='/rules/deny/')
@csrf_exempt  # not secure
def add_rule_api(request):
    """API: Add an alerting rule."""
    if not request.method == 'POST':
        return JsonResponse(
            {'status': 'error'}, json_dumps_params={'indent': 2}, status=403)

    params = json.loads(request.body)
    new_rule_args = {
        "title": params["title"],
        "scope": params["scope"],
        "scope_attr": params["scope_attr"],
        "condition": {params["condition"]: params["criteria"]},
        "enabled": params["enable"] == "enabled",
#        "severity": params["severity"],
        "trigger": params["trigger"],
        "target": params["target"],
        "owner": request.user
    }
    new_rule = Rule.objects.create(**new_rule_args)
    new_rule.save()
    messages.success(request, 'Regra criada com sucesso!')

    return JsonResponse({'status': 'success'}, json_dumps_params={'indent': 2})



# Add Bloqueio de URL - By BILL
@user_passes_test(lambda u: u.groups.filter(name='visitante').count() == 0, login_url='/rules/deny/')
@user_passes_test(lambda u: u.groups.filter(name='analista').count() == 0,  login_url='/rules/deny/')
@user_passes_test(lambda u: u.groups.filter(name='dpo').count() == 0, login_url='/rules/deny/')
@csrf_exempt  # not secure
def toggle_rule_status_api(request, rule_id):
    """API: Change status of an alerting rule."""
    rule = get_object_or_404(Rule, id=rule_id)
    rule.enabled = not rule.enabled
    rule.save()
    return JsonResponse({'status': 'success'}, json_dumps_params={'indent': 2})



# Add Bloqueio de URL - By BILL
@user_passes_test(lambda u: u.groups.filter(name='visitante').count() == 0, login_url='/rules/deny/')
@user_passes_test(lambda u: u.groups.filter(name='analista').count() == 0,  login_url='/rules/deny/')
@user_passes_test(lambda u: u.groups.filter(name='dpo').count() == 0, login_url='/scans/deny/')
def duplicate_rule_api(request, rule_id):
    """API: Duplicate an alerting rule."""
    new_rule = get_object_or_404(Rule, id=rule_id)
    new_rule.title = new_rule.title + " (copy)"
    new_rule.pk = None
    new_rule.save()
    return JsonResponse({'status': 'success'}, json_dumps_params={'indent': 2})

# Slack  Fix - By Bill


# Add Bloqueio de URL - By BILL
@user_passes_test(lambda u: u.groups.filter(name='visitante').count() == 0, login_url='/rules/deny/')
@user_passes_test(lambda u: u.groups.filter(name='analista').count() == 0,  login_url='/rules/deny/')
@user_passes_test(lambda u: u.groups.filter(name='dpo').count() == 0, login_url='/rules/deny/')
def send_slack_message_api(request):  # test purposes
    """API: Send a Slack message."""
    slack_url = get_object_or_404(Setting, key="alerts.endpoint.slack.webhook")
    alert_message = "[Alert] This is a test message"

    requests.post(
        slack_url.value,
        data=json.dumps({'text': alert_message}),
        headers={'content-type': 'application/json'})
    return JsonResponse({'status': 'success'}, json_dumps_params={'indent': 2})

 # HG Fix - By Bill


# Add Bloqueio de URL - By BILL
@user_passes_test(lambda u: u.groups.filter(name='visitante').count() == 0, login_url='/rules/deny/')
@user_passes_test(lambda u: u.groups.filter(name='analista').count() == 0,  login_url='/rules/deny/')
@user_passes_test(lambda u: u.groups.filter(name='dpo').count() == 0, login_url='/rules/deny/')
def send_hostsgreen_message_api(request):  # test purposes
    """API: Send a HG  message."""
    hostsgreen_url = get_object_or_404(Setting, key="alerts.endpoint.hostsgreen.webhook")
    alert_message = "[Alert] This is a test message"

    requests.post(
        hostsgreen_url.value,
        data=json.dumps({'text': alert_message}),
        headers={'content-type': 'application/json'})
    return JsonResponse({'status': 'success'}, json_dumps_params={'indent': 2})

