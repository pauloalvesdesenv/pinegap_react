# -*- coding: utf-8 -*-
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Finding, RawFinding
from .forms import ImportFindingsForm, FindingForm
from .utils import _search_findings
from assets.models import Asset
from events.models import Event
from engines.tasks import importfindings_task
import json
import os
import time
import collections

##############Implement Control Access of Url - By BILL##############
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404

######################################################################

def list_findings_view(request):
    findings = _search_findings(request)

    nb_findings = findings.count()

    # Pagination findings
    nb_rows = request.GET.get('n', 50)
    findings_paginator = Paginator(findings, nb_rows)
    page = request.GET.get('page')
    try:
        findings_p = findings_paginator.page(page)
    except PageNotAnInteger:
        findings_p = findings_paginator.page(1)
    except EmptyPage:
        findings_p = findings_paginator.page(findings_paginator.num_pages)

    return render(request, 'list-findings.html', {
        'findings': findings_p, 'nb_findings': nb_findings})


def list_asset_findings_view(request, asset_name):
    findings = None
    filter_by_status = request.GET.get('_status', None)

    filters = {
        "asset_name": asset_name
    }
    if filter_by_status and filter_by_status in ["new", "ack"]:
        filters.update({"status": filter_by_status})

    findings = Finding.objects.filter(**filters).order_by(
             'asset_name', 'severity', 'status', 'type')

    return render(request, 'list-findings.html', {'findings': findings})


# Add Bloqueio de URL - By BILL
@user_passes_test(lambda u: u.groups.filter(name='visitante').count() == 0, login_url='/findings/deny/')
@user_passes_test(lambda u: u.groups.filter(name='analista').count() == 0,  login_url='/findings/deny/')
@user_passes_test(lambda u: u.groups.filter(name='dpo').count() == 0, login_url='/findings/deny/')
def delete_finding_view(request, finding_id):
    finding = get_object_or_404(Finding, id=finding_id)
    asset_id = finding.asset.id
    finding.delete()

    # reevaluate related asset critity
    Asset.objects.get(owner_id=request.user.id, asset_id=finding.asset_id).evaluate_risk()
    Asset.objects.get(id=asset_id).evaluate_risk()
    messages.success(request, 'Ocorr&ecirc;ncia apagada com sucesso!')
    return redirect('list_findings_view')



# Add Bloqueio de URL - By BILL
@user_passes_test(lambda u: u.groups.filter(name='visitante').count() == 0, login_url='/findings/deny/')
@user_passes_test(lambda u: u.groups.filter(name='analista').count() == 0,  login_url='/findings/deny/')
@user_passes_test(lambda u: u.groups.filter(name='dpo').count() == 0, login_url='/findings/deny/')
def import_findings_view(request):
    if request.method == 'POST':
        form = ImportFindingsForm(request.POST, request.FILES)

        if form.is_valid():
            # store the file in /media/imports/<owner_id>/<tmp_file>
            user_report_dir = settings.MEDIA_ROOT + "/imports/"+str(request.user.id)+"/"
            if not os.path.exists(user_report_dir):
                os.makedirs(user_report_dir)
            filename = user_report_dir+"import_" + str(request.user.id) + "_" + str(int(time.time() * 1000)) + "." + form.cleaned_data['engine']
            with open(filename, 'wb+') as destination:
                for chunk in request.FILES['file'].chunks():
                    destination.write(chunk)
            # enqueue the import processing
            importfindings_task.apply_async(
                args=[filename, request.user.id, form.cleaned_data['engine'], form.cleaned_data['min_level']],
                queue='default',
                routing_key='default',
                retry=False
            )

            messages.success(request, 'Ocorr&ecirc;ncia importada com sucesso!')
        return redirect('list_findings_view')
    else:
        form = ImportFindingsForm()
    return render(request, 'import-findings.html', {'form': form})


def details_finding_view(request, finding_id):
    finding = None

    if request.GET.get("raw", None) and request.GET.get("raw") == "true":
        finding = get_object_or_404(RawFinding, id=finding_id)
        return render(request, 'details-finding.html', {'finding': finding, 'raw': True})

    finding = get_object_or_404(Finding, id=finding_id)

    # Inject tracking data
    tracking_timeline = {}
    tracking_timeline.update({finding.created_at: {"level": "info", "message": "Vulnerabilidade primeiramente encontrada no scan <a href='/scans/details/{}'>'{}'</a> ({}). Ver detalhes <a href='/scans/defs/details/{}'>(Click AQUI)</a>".format(finding.scan.id, finding.scan, finding.scan.engine_type, finding.scan.scan_definition.id)}})

    # Identify changes
    for event in Event.objects.filter(finding=finding):
        tracking_timeline.update({event.created_at: {"level": "info", "message": event.message}})

    # Identify finding occurrences in related scan results (excluding the 1st)
    for scan in finding.scan.scan_definition.scan_set.filter(status="finished").exclude(id=finding.scan.id):
        finding_notfound = True
        for f in scan.rawfinding_set.all():
            if f.hash == finding.hash:
                finding_notfound = False
                tracking_timeline.update({f.created_at: {
                    "level": "info",
                    "message": "Identificada no scan <a href='/scans/details/{}'>{}</a>".format(scan.id, scan)}})
            break
        if finding_notfound:
            tracking_timeline.update({scan.created_at: {
                "level": "warning",
                "message": "Esta mesma ocorr&ecirc;ncia para este mesmo ativo, foi encontrada no scan  <a  href='/scans/details/{}'>{} - (Clique Aqui)</a>".format(scan.id, scan)}})

    return render(request, 'details-finding.html', {
        'finding': finding,
        'raw': False,
        'tracking_timeline': collections.OrderedDict(sorted(tracking_timeline.items(), key=lambda t: t[0]))})




# Add Bloqueio de URL - By BILL
@user_passes_test(lambda u: u.groups.filter(name='visitante').count() == 0, login_url='/findings/deny/')
@user_passes_test(lambda u: u.groups.filter(name='dpo').count() == 0, login_url='/findings/deny/')
def edit_finding_view(request, finding_id):
    form = None
    is_raw_finding = request.GET.get("raw", None) and request.GET.get("raw") == "true"
    if is_raw_finding:
        finding = get_object_or_404(RawFinding, id=finding_id)
    else:
        finding = get_object_or_404(Finding, id=finding_id)

    form = FindingForm()
    if request.method == 'GET':
        form = FindingForm(instance=finding)
    elif request.method == 'POST':
        form = FindingForm(request.POST, instance=finding)

        if form.is_valid():
            finding.title = form.cleaned_data['title']
            finding.description = form.cleaned_data['description']
            finding.type = form.cleaned_data['type']
            finding.severity = form.cleaned_data['severity']
            finding.solution = form.cleaned_data['solution']
            finding.risk_info = form.cleaned_data['risk_info']
            finding.vuln_refs = form.cleaned_data['vuln_refs']
            finding.links = form.cleaned_data['links']
            finding.tags = form.cleaned_data['tags']
            finding.status = form.cleaned_data['status']
            finding.comments = form.cleaned_data['comments']
#Modificação para atender  redirecionamento de tela para  novas ocorrencias apos edicao.
            finding.save()
            messages.success(request, 'Ocorr&ecirc;ncia tratada com sucesso!')
#            return redirect('list_findings_view')
            return redirect ('/findings/list?_status=new')
#            return render(request, 'list-findings.html')
    return render(request, 'edit-finding.html',
        {'form': form, 'finding': finding, 'raw': is_raw_finding})



# Add Bloqueio de URL - By BILL
@user_passes_test(lambda u: u.groups.filter(name='visitante').count() == 0, login_url='/findings/deny/')
@user_passes_test(lambda u: u.groups.filter(name='analista').count() == 0,  login_url='/findings/deny/')
@user_passes_test(lambda u: u.groups.filter(name='dpo').count() == 0, login_url='/findings/deny/')
def add_finding_view(request):
    form = None

    form = FindingForm()
    if request.method == 'GET':
        form = FindingForm()
    elif request.method == 'POST':
        form = FindingForm(request.POST)

        if form.is_valid():
            finding_args = {
                'title': form.cleaned_data['title'],
                'description': form.cleaned_data['description'],
                'confidence': form.cleaned_data['confidence'],
                'type': form.cleaned_data['type'],
                'severity': form.cleaned_data['severity'],
                'solution': form.cleaned_data['solution'],
                'risk_info': form.cleaned_data['risk_info'],
                'vuln_refs': form.cleaned_data['vuln_refs'],
                'links': form.cleaned_data['links'],
                'tags': str(json.dumps(form.cleaned_data['tags'].split(','))),
                'status': form.cleaned_data['status'],
                'owner': form.cleaned_data['owner'],
                'asset': form.cleaned_data['asset'],
                'asset_name': form.cleaned_data['asset'].value,
                'scan': form.cleaned_data['scan']
            }

            finding = Finding(**finding_args)
            finding.save()
            messages.success(request, 'Ocorr&ecirc;ncia criada com sucesso!')
            return redirect('list_findings_view')

    return render(request, 'add-finding.html', {'form': form})


def compare_findings_view(request):
    finding_a_id = request.GET.get("finding_a_id", None)
    finding_b_id = request.GET.get("finding_b_id", None)
    raw_finding = request.GET.get("raw", None)
    if raw_finding:
        finding_a = get_object_or_404(RawFinding, id=finding_a_id)
        finding_b = get_object_or_404(RawFinding, id=finding_b_id)
    else:
        finding_a = get_object_or_404(Finding, id=finding_a_id)
        finding_b = get_object_or_404(Finding, id=finding_b_id)

    return render(request, 'compare-findings.html', {
        'finding_a': finding_a,
        'finding_b': finding_b})



