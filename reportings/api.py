# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.http import JsonResponse, HttpResponse, QueryDict #Billing
from django.forms.models import model_to_dict #Billing
from django.utils.encoding import smart_str #Billing
from django.db.models import Value, CharField, Q #Billing
from django.shortcuts import render, redirect, get_object_or_404 #Billing
from django.core.files.storage import FileSystemStorage # Billing
from wsgiref.util import FileWrapper # Billing
from rest_framework.decorators import api_view # Billing
from assets.models import Asset, AssetGroup, AssetCategory #Billing
from assets.models import AssetOwner, AssetOwnerContact, AssetOwnerDocument #Billing
from assets.models import ASSET_CRITICITIES #Billing
from assets.forms import AssetOwnerContactForm, AssetOwnerDocumentForm #Billing
from events.models import Event #Billing
from django.utils import timezone as tz #Billing

from assets.models import Asset, AssetGroup
from findings.models import Finding
from django.views.decorators.csrf import csrf_exempt #Billing
import json 		#Billing
import csv 		#Billing
import os 		#Billing
import mimetypes	#Billing
import datetime 	#Billing
import urllib 		#Billing




def global_stats_api(request):
    data = None
    return JsonResponse(data)

def dashboard_resumido_api(request):
    data = None
    return JsonResponse(data)



#Recuperar Ativos deletados em Eventos
@api_view(['GET'])
def deleted_assets_api(request):
    """List Events."""
    events = []
    for e in Event.objects.filter(type="DELETE", message__startswith="[Asset] Ativo").order_by('created_at'):
        events.append(model_to_dict(e))

    return JsonResponse(events, json_dumps_params={'indent': 2}, safe=False)


#Historico de datas de Ativos criados deletados em Eventos
@api_view(['GET'])
def history_assets_api(request):
    """List Events."""
    events = []
    for e in Event.objects.filter(type="CREATE", message__startswith="[Asset]"):
        events.append(model_to_dict(e))

    return JsonResponse(events, json_dumps_params={'indent': 2}, safe=False)

# Add Matriz Risco Quantitativo
api_view(['GET'])
def matriz_risco_quantitativo_api(request):
    risk_c
    risk_value_c = Asset.objects.filter(risk_level__grade="C").aggregate(Sum('financeiro'))['financeiro__sum'],

    return JsonResponse(risk_c, json_dumps_params={'indent': 2}, safe=False)





@api_view(['GET'])
def using_assets_api(request):
    q = request.GET.get("q", None)
    if q:
        assets = list(Asset.objects
            .filter(Q(value__icontains=q) | Q(name__icontains=q))
            .annotate(format=Value("asset", output_field=CharField()))
            .values('id', 'value', 'format', 'name', 'type', 'created_at'))
        assetgroups = list(AssetGroup.objects.filter(name__icontains=q)
            .extra(select={'value': 'name'})
            .annotate(format=Value("assetgroup", output_field=CharField()))
            .values('id', 'value', 'format', 'name'))
    else:
        assets = list(Asset.objects
            .annotate(format=Value("asset", output_field=CharField()))
            .values('id', 'value', 'format', 'name', 'type', 'created_at'))
        assetgroups = list(AssetGroup.objects
            .extra(select={'value': 'name'})
            .annotate(format=Value("assetgroup", output_field=CharField()))
            .values('id', 'value', 'format', 'name'))
    return JsonResponse(assets + assetgroups, safe=False)


@api_view(['GET'])
def billing_statement_api(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)

    findings_tmp = list()
    findings_stats = {}

    # @todo: invert loops
    for sev in ["critical", "high", "medium", "low", "info"]:
        tmp = Finding.objects.filter(asset=asset.id, severity=sev).order_by('type')
        if tmp.count() > 0:
            findings_tmp += tmp
        findings_stats.update({sev: tmp.count()})
    findings_stats.update({"total": len(findings_tmp)})

    return render(request, 'report-asset-statement.html', {
        'asset': asset,
        'findings': findings_tmp,
        'findings_stats': findings_stats})
