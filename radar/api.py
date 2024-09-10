#from django.http import JsonResponse
#from assets.models import Asset, AssetGroup
#from findings.models import Finding
from django.http import JsonResponse
from assets.models import Asset, AssetGroup
from findings.models import Finding
from rest_framework.decorators import api_view
from django.forms.models import model_to_dict
from django.shortcuts import render, get_object_or_404

from scans.models import Scan, ScanDefinition
from findings.models import RawFinding

from datetime import timedelta
from pytz import timezone
import datetime
import json
import os
import tempfile


def global_stats_api(request):
    data = None
    return JsonResponse(data)

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
         #  "nb_time_minutes": ScanDefinition.objects.filter(period='minutes', scan_type='periodic'),
         #  "nb_time_hours": ScanDefinition.objects.filter(period='hours', scan_type='periodic'),
         #  "nb_time_seconds": ScanDefinition.objects.filter(period='seconds', scan_type='periodic'),
         #  "nb_time_days": ScanDefinition.objects.filter(period='days', scan_type='periodic'),
         #  "nb_recorrency": ScanDefinition.objects.filter(every=0, scan_type='periodic'),
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
