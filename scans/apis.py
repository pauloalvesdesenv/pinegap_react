# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import JsonResponse, HttpResponse
from wsgiref.util import FileWrapper
from django.shortcuts import render, get_object_or_404
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django_celery_beat.models import PeriodicTask
from rest_framework.decorators import api_view

from .models import Scan, ScanDefinition
from .utils import _update_celerybeat, _run_scan, _search_scans, _add_scan_def
from engines.tasks import stopscan_task
from findings.models import RawFinding

from datetime import timedelta
from pytz import timezone
import datetime
import json
import os
import tempfile
import zipfile
import csv
import tzlocal


@api_view(['GET'])
def get_scan_definitions_api(request):
    """Get scan definitions."""
    scans_list = []
    for scan in ScanDefinition.objects.all():
        scans_list.append(scan.to_dict())
    return JsonResponse(scans_list, safe=False)


@api_view(['GET'])
def get_scan_definition_api(request, scan_id):
    """Get selected scan."""
    scan = get_object_or_404(ScanDefinition, id=scan_id)
    return JsonResponse(scan.to_dict(), safe=False)


@api_view(['GET'])
def get_scan_api(request, scan_id):
    """Get selected scan."""
    scan = get_object_or_404(Scan, id=scan_id)
    return JsonResponse(scan.to_dict(), safe=False)


@api_view(['GET'])
def get_scans_api(request):
    """Get scans."""
    scans_list = []
    for scan in _search_scans(request):
        scans_list.append(scan.to_dict())
    return JsonResponse(scans_list, safe=False)


@api_view(['GET', 'DELETE'])
def delete_scan_api(request, scan_id):
    """Delete selected scan."""
    scan = get_object_or_404(Scan, id=scan_id)
    scan.delete()
    return JsonResponse({'status': 'success'})


@api_view(['POST', 'DELETE'])
def delete_scans_api(request):
    """Delete selected scans."""
    scans = request.data
    for scan_id in scans:
        Scan.objects.get(id=scan_id).delete()
    return JsonResponse({'status': 'success'})



@api_view(['GET', 'DELETE'])
def delete_scan_def_api(request, scan_id):
    """Delete selected scan defs."""
    scan = get_object_or_404(ScanDefinition, id=scan_id)
    scan.delete()
    return JsonResponse({'status': 'success'})


@api_view(['GET'])
def stop_scan_api(request, scan_id):
    """Stop a scan."""
    scan = get_object_or_404(Scan, id=scan_id)
    scan.status = "stopping"
    scan.save()
    stopscan_task.apply_async(
        args=[scan.id], queue='scan', retry=True, ignore_result=False)
    # args=[scan.id], queue='scan', retry=False, ignore_result=True)
    return JsonResponse({'status': 'success'})


@api_view(['POST'])
def stop_scans_api(request):
    """Stop selected scans."""
    scans = request.data
    for scan_id in scans:
        try:
            scan = Scan.objects.get(id=scan_id)
        except Scan.DoesNotExist:
            continue

        scan.status = "stopping"
        scan.save()
        stopscan_task.apply_async(
            args=[scan.id],
            queue='scan',
            retry=True,
            ignore_result=True
        )

    return JsonResponse({'status': 'success'})


@api_view(['GET'])
def get_scans_stats_api(request):
    scope = request.GET.get('scope', None)
    data = {}
    if not scope:
        scan_defs = ScanDefinition.objects.all()
        scans = Scan.objects.all()
        data = {
            "nb_scans_defined": scan_defs.count(),
            "nb_scans_performed": scans.count(),
            "nb_periodic_scans": scan_defs.filter(scan_type="periodic").count(),
            "nb_active_periodic_scans": scan_defs.filter(scan_type="periodic", enabled=True).count()
        }
    elif scope == "scan_def":
        scan_id = request.GET.get('scan_id', None)
        num_records = request.GET.get('num_records', 10)
        if not scan_id:
            return JsonResponse({})
        # scan_def = get_object_or_404(ScanDefinition, id=scan_id)
        scans = reversed(Scan.objects.filter(scan_definition=scan_id).values('id', 'created_at', 'summary').order_by('-created_at')[:num_records])
        data = list(scans)
    elif scope == "scans":
        num_records = request.GET.get('num_records', 10)
        scans = reversed(Scan.objects.all().values('id', 'created_at', 'summary').order_by('-created_at')[:num_records])
        data = list(scans)

    return JsonResponse(data, json_dumps_params={'indent': 2}, safe=False)


@api_view(['GET'])
def get_scans_heatmap_api(request):
    data = {}

    for scan in Scan.objects.all():
        # expected format: {timestamp: value, timestamp2: value2 ...}
        # data.update({scan.updated_at.astimezone(timezone('Europe/Paris')).strftime("%s"): 1})
        data.update({scan.updated_at.astimezone(tzlocal.get_localzone()).strftime("%s"): 1})
    return JsonResponse(data)


@api_view(['GET'])
def get_scans_by_period_api(request):
    # remove to optimize

    data = {}
    start_date = request.GET.get('start', None)
    stop_date = request.GET.get('stop', None)
    if start_date and datetime.strptime(start_date, '%Y-%m-%dT%H:%M:%fZ'):
        start_date = datetime.strptime(start_date, '%Y-%m-%dT%H:%M:%fZ')
    if stop_date:
        stop_date = datetime.strptime(stop_date, '%Y-%m-%dT%H:%M:%fZ')

    for scan in Scan.objects.filter(updated_at__gte=start_date):
        # expected format: {timestamp: value, timestamp2: value2 ...}
        data.update({scan.updated_at.strftime("%s"): 1})
    return JsonResponse(data)


@api_view(['GET'])
def get_scans_by_date_api(request):
    scopes = ["year", "month", "week", "day", "hour", "minute"]
    data = []
    date = request.GET.get('date', None)
    stop_date = None
    scope = request.GET.get('scope', None)
    if date and datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%fZ'):
        date_wot = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%fZ')
        date = timezone(tzlocal.get_localzone().zone).localize(date_wot)
    else:
        return HttpResponse(status=400)

    if scope not in scopes:
        return HttpResponse(status=400)

    if scope == "hour":
        stop_date = date + timedelta(hours=1)
    elif scope == "day":
        stop_date = date + timedelta(days=1)
    elif scope == "week":
        stop_date = date + timedelta(days=7)
    elif scope == "month":
        stop_date = date + timedelta(days=30)

    scans = Scan.objects.filter(updated_at__gte=date, updated_at__lte=stop_date)
    for scan in scans:
        data.append({
            'scan_id': scan.id,
             "status": scan.status,
             "engine_type": scan.engine_type.name,
             "title": scan.title,
             "summary": json.dumps(scan.summary),
             "updated_at": scan.updated_at,
             "scan_definition_id": scan.scan_definition.id
        })
    return JsonResponse(data, safe=False)


@api_view(['GET'])
def get_scan_report_html_api(request, scan_id):
    scan = get_object_or_404(Scan, id=scan_id)
    tmp_scan = model_to_dict(scan)
    tmp_scan['assets'] = []
    for asset in scan.assets.all():
        tmp_scan['assets'].append(asset.value)

    tmp_scan['engine_type_name'] = scan.engine_type.name
    tmp_scan['engine_name'] = scan.engine.name
    tmp_scan['engine_policy_name'] = scan.engine_policy.name

    findings = RawFinding.objects.filter(scan=scan.id)

    findings_tmp = list()
    for sev in ["high", "medium", "low", "info", "critical"]:
        tmp = RawFinding.objects.filter(scan=scan, severity=sev).order_by('type')
        if tmp.count() > 0:
            findings_tmp += tmp

    findings_by_asset = dict()
    for asset in scan.assets.all():
        findings_by_asset_tmp = list()
        for sev in ["critical", "high", "medium", "low", "info"]:
            tmp = RawFinding.objects.filter(scan=scan, asset=asset, severity=sev).order_by('type')
            if tmp.count() > 0:
                findings_by_asset_tmp += tmp
        findings_by_asset.update({asset.value: findings_by_asset_tmp})

    findings_stats = {
        "total": findings.count(),
        "high": findings.filter(severity='high').count(),
        "medium": findings.filter(severity='medium').count(),
        "low": findings.filter(severity='low').count(),
        "info": findings.filter(severity='info').count(),
        "critical": findings.filter(severity='critical').count()
    }

    for asset in scan.assets.all():
        findings_stats.update({
            asset.value: {
                "total": findings.filter(asset=asset).count(),
                "critical": findings.filter(asset=asset, severity='critical').count(),
                "high": findings.filter(asset=asset, severity='high').count(),
                "medium": findings.filter(asset=asset, severity='medium').count(),
                "low": findings.filter(asset=asset, severity='low').count(),
                "info": findings.filter(asset=asset, severity='info').count(),
            }
        })

    return render(request, 'report-scan.html', {
        'scan': tmp_scan,
        'findings': findings_by_asset,
        'findings_stats': findings_stats})


@api_view(['GET'])
def get_scan_report_json_api(request, scan_id):
    scan = get_object_or_404(Scan, id=scan_id)

    filename = str(scan.report_filepath)
    if not os.path.isfile(filename):
        return HttpResponse(status=404)

    wrapper = FileWrapper(file(filename))
    response = HttpResponse(wrapper, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=report_'+os.path.basename(filename)
    response['Content-Length'] = os.path.getsize(filename)

    return response


@api_view(['GET'])
def get_scan_report_csv_api(request, scan_id):
    scan = get_object_or_404(Scan, id=scan_id)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=report_{}.csv'.format(scan_id)

    writer = csv.writer(response, delimiter=str(';'))
    writer.writerow([
        'endereço', 'tipo_do_ativo',
        'tipo_de_sensor', 'nome_do_sensor',
        'nome_do_scan', 'scan_policy',
        'finding_id', 'finding_title', 'finding_type', 'finding_status',
        'finding_severity', 'finding_description',
        'finding_solution', 'finding_hash', 'finding_creation_date',
        'finding_risk_info', 'finding_cvss',
        ])

    for finding in RawFinding.objects.filter(scan=scan).order_by('asset__name', 'severity', 'title'):
        writer.writerow([
            finding.asset.value, finding.asset.type,
            scan.engine_type.name, scan.engine.name,
            scan.title, scan.engine_policy.name,
            finding.id, finding.title, finding.type, finding.status,
            finding.severity, finding.description,
            finding.solution, finding.hash, finding.created_at,
            finding.risk_info, finding.risk_info['cvss_base_score']
        ])

    return response


@api_view(['GET'])
def send_scan_reportzip_api(request, scan_id):
    scan = get_object_or_404(Scan, id=scan_id)

    filename = str(scan.report_filepath)
    temp = tempfile.TemporaryFile()
    archive = zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED)
    archive.write(filename)
    archive.close()
    wrapper = FileWrapper(temp)
    response = HttpResponse(wrapper, content_type='application/zip')
    response['Content-Disposition'] = "attachment; filename=scan_report_{}.zip".format(scan_id)
    response['Content-Length'] = temp.tell()
    temp.seek(0)
    return response


@csrf_exempt
@api_view(['GET'])
def toggle_scan_def_status_api(request, scan_def_id):
    scan_def = get_object_or_404(ScanDefinition, id=scan_def_id)
    scan_def.enabled = not scan_def.enabled
    scan_def.save()

    if scan_def.scan_type == 'periodic':
        try:
            periodic_task = scan_def.periodic_task
            periodic_task.enabled = scan_def.enabled
            periodic_task.last_run_at = None
            periodic_task.save()
            # Todo: wait celery beat fix
            _update_celerybeat()
        except PeriodicTask.DoesNotExist:
            print ("Fuck, PeriodicTask '{}' does not exists".format(periodic_task.id))
            return JsonResponse({'status': 'error'}, 403)

    return JsonResponse({'status': 'success'})


@api_view(['GET'])
def run_scan_def_api(request, scan_def_id):
    scan_def = get_object_or_404(ScanDefinition, id=scan_def_id)

    if scan_def.scan_type in ["single", "scheduled"]:
        _run_scan(scan_def_id, request.user.id)
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'failed'}, status=403)


@api_view(['POST', 'PUT'])
def add_scan_def_api(request):
    scan_def = _add_scan_def(request.data, owner=request.user)
    if scan_def:
        return JsonResponse({'status': 'success', 'scan_def_id': scan_def.id})
    else:
        return JsonResponse({'status': 'failed'}, status=403)
    