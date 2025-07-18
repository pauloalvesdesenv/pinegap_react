# -*- coding: utf-8 -*-

from django.http import JsonResponse, HttpResponse, QueryDict
from django.forms.models import model_to_dict
from django.utils.encoding import smart_str
from django.db.models import Value, CharField, Q
from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import FileSystemStorage

from wsgiref.util import FileWrapper
from rest_framework.decorators import api_view

from .models import Asset, AssetGroup, AssetCategory
from .models import AssetOwner, AssetOwnerContact, AssetOwnerDocument
from .models import ASSET_CRITICITIES
from .forms import AssetOwnerContactForm, AssetOwnerDocumentForm
from app.settings import MEDIA_ROOT
from findings.models import Finding
from events.models import Event
from django.utils import timezone as tz
from django.views.decorators.csrf import csrf_exempt


import json
import csv
import os
import mimetypes
import datetime
import urllib
from django.db.models import Case, When
from django.contrib.postgres.aggregates import ArrayAgg
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.serializers.json import DjangoJSONEncoder




#Eventos
@api_view(['GET'])
def deleted_assets_api(request):
    """List Events."""
    events = []
    for e in Event.objects.filter(type="DELETE", message__contains="[Asset] Ativo"):
        events.append(model_to_dict(e))

    return JsonResponse(events, json_dumps_params={'indent': 2}, safe=False)



# Assets
@api_view(['GET'])
def get_asset_api(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)
    return JsonResponse(asset.to_dict(), safe=False)


@api_view(['GET'])
def get_asset_findings_api(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)
    findings = [f.to_dict() for f in asset.finding_set.all()]
    return JsonResponse(findings, safe=False)


@api_view(['GET'])
def get_assets_stats_api(request):
    assets = Asset.objects.all()
    data = {
        "nb_assets": assets.count(),
        "nb_assets_high": assets.filter(criticity="high").count(),
        "nb_assets_medium": assets.filter(criticity="medium").count(),
        "nb_assets_low": assets.filter(criticity="low").count()
    }
    return JsonResponse(data)


@api_view(['GET'])
def get_asset_details_api(request, asset_name):
    asset = get_object_or_404(Asset, value=asset_name)

    # Asset details
    response = model_to_dict(asset, fields=[field.name for field in asset._meta.fields])

    # Related asset groups
    asset_groups = []
    for asset_group in asset.assetgroup_set.all():
        asset_group_dict = model_to_dict(asset_group, fields=[field.name for field in asset_group._meta.fields])
        asset_groups.append(asset_group_dict)
    response.update({
        "asset_groups": asset_groups
    })

    # Related findings
    findings = []
    for finding in asset.finding_set.all():
        finding_dict = model_to_dict(finding, fields=[field.name for field in finding._meta.fields])
        findings.append(finding_dict)
    response.update({
        "findings": findings
    })

    # Last 10 scans
    scans = []
    for scan in asset.scan_set.all()[:10]:
        scan_dict = model_to_dict(scan, fields=[field.name for field in scan._meta.fields])
        scans.append(scan_dict)

    response.update({
        "last10scans": scans
    })

    return JsonResponse(response, json_dumps_params={'indent': 2}, safe=False)


@api_view(['GET'])
def get_asset_trends_api(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)
    data = []
    ticks_by_period = {'week': 7, 'month': 30, 'bimestre': 60, 'trimester': 90, 'quadrimester': 120, 'quimestre': 150, 'semester': 180, 'year': 365}
    grade_levels = {'A': 6, 'B': 5, 'C': 4, 'D': 3, 'E': 2, 'F': 1, 'n/a': 0}

    # period = x-axis
    period = request.GET.get('period_by', None)
    if period not in ticks_by_period.keys():
        period = 7
    else:
        period = ticks_by_period[period]

    nb_ticks = int(request.GET.get('max_ticks', 15))
    if nb_ticks < period:
        delta = period // nb_ticks
    else:
        delta = 1

    startdate = datetime.datetime.today()
    for i in range(0, nb_ticks):
        enddate = startdate - datetime.timedelta(days=i*delta)
        findings_stats = {
            'total': 0,
            'critical': 0, 'high': 0, 'medium': 0, 'low': 0, 'info': 0,
            'new': 0,
            'risk_grade': 'n/a',
            'date': str(enddate.date())}
        for f in asset.finding_set.filter(created_at__lte=enddate):
            findings_stats['total'] = findings_stats.get('total') + 1
            findings_stats[f.severity] = findings_stats.get(f.severity) + 1
            if f.status == 'new':
                findings_stats['new'] = findings_stats.get('new') + 1

        if findings_stats['total'] != 0:
            findings_stats['risk_grade'] = grade_levels[asset.get_risk_grade(history=i)]
            # findings_stats['risk_grade'] = grade_levels[asset.get_risk_grade(history=i)['grade']]
        else:
            findings_stats['risk_grade'] = 0
        data.append(findings_stats)

    return JsonResponse(data[::-1], json_dumps_params={'indent': 2}, safe=False)


@api_view(['GET'])
def list_assets_api(request):
    q = request.GET.get("q", None)
    if q:
        assets = list(Asset.objects
            .filter(Q(value__icontains=q) | Q(name__icontains=q))
            .annotate(format=Value("asset", output_field=CharField()))
            .values('id', 'value', 'format', 'name'))
        assetgroups = list(AssetGroup.objects.filter(name__icontains=q)
            .extra(select={'value': 'name'})
            .annotate(format=Value("assetgroup", output_field=CharField()))
            .values('id', 'value', 'format', 'name'))
    else:
        assets = list(Asset.objects
            .annotate(format=Value("asset", output_field=CharField()))
            .values('id', 'value', 'format', 'name'))
        assetgroups = list(AssetGroup.objects
            .extra(select={'value': 'name'})
            .annotate(format=Value("assetgroup", output_field=CharField()))
            .values('id', 'value', 'format', 'name'))
    return JsonResponse(assets + assetgroups, safe=False)



@api_view(['GET'])
def list_all_assets_api(request):
    q = request.GET.get("q", None)
    if q:
        assets = list(Asset.objects
            .filter(Q(value__icontains=q) | Q(name__icontains(q)))
            .values())
    else:
        assets = list(Asset.objects.values())
    return JsonResponse(assets, safe=False)

@api_view(['GET'])
def list_all_group_assets_api(request):
    q = request.GET.get("q", None)
    if q:
        asset_groups = list(AssetGroup.objects
            .filter(Q(name__icontains=q))
            .values())
    else:
        asset_groups = list(AssetGroup.objects.values())
    return JsonResponse(asset_groups, safe=False)


class AssetCategoryEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, AssetCategory):
            return model_to_dict(obj)
        return super(AssetCategoryEncoder, self).default(obj)
    
class AssetEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Asset):
            return model_to_dict(obj)
        return super(AssetEncoder, self).default(obj)

@api_view(['GET'])
def list_assets_detailed_api(request):
    # Check sorting options
    allowed_sort_options = ["id", "name", "criticity_num", "financeiro", "score", "type",
                            "updated_at", "created_at", "risk_level", "risk_level__grade",
                            "-id", "-name", "-criticity_num", "-financeiro", "-score","-created_at",
                            "-type", "-updated_at", "-risk_level",
                            "-risk_level__grade"]

    sort_options = request.GET.get("sort", "-updated_at")
    sort_options_valid = []
    for s in sort_options.split(","):
        if s in allowed_sort_options and s not in sort_options_valid:
            sort_options_valid.append(str(s))

    # Check Filtering options
    filter_options = request.GET.get("filter", "")

    # Todo: filter on fields - risco quantitativo - "financeiro"
    allowed_filter_fields = ["id", "name", "criticity", "financeiro", "type", "score"]
    filter_criterias = filter_options.split(" ")
    filter_fields = {}
    filter_opts = ""
    for criteria in filter_criterias:
        field = criteria.split(":")
        if len(field) > 1 and field[0] in allowed_filter_fields:
            # allowed field
            if field[0] == "score":
                filter_fields.update({"risk_level__grade": field[1]})
            else:
                filter_fields.update({str(field[0]): field[1]})
        else:
            filter_opts = filter_opts + str(criteria.strip())

    # Query
    assets_list = Asset.objects.filter(**filter_fields).filter(
        Q(value__icontains=filter_opts) |
        Q(name__icontains=filter_opts) |
        Q(description__icontains=filter_opts)
        ).annotate(
            criticity_num=Case(
                When(criticity="high", then=Value("1")),
                When(criticity="medium", then=Value("2")),
                When(criticity="low", then=Value("3")),
                default=Value("1"),
                output_field=CharField())
            ).annotate(cat_list=ArrayAgg('categories__value')).order_by(*sort_options_valid)

    # Pagination assets - Modificado Python3
    nb_rows = request.GET.get('n', 16)
    assets_paginator = Paginator(assets_list, nb_rows)
    page = request.GET.get('page')
    try:
        assets = assets_paginator.page(page)
    except PageNotAnInteger:
        assets = assets_paginator.page(1)
    except EmptyPage:
        assets = assets_paginator.page(assets_paginator.num_pages)

    # Convert assets to list of dictionaries
    assets_serialized = []
    for asset in assets:
        asset_dict = model_to_dict(asset)
        asset_dict['categories'] = [category.to_dict() for category in asset.categories.all()]
        asset_dict['criticity_num'] = asset.criticity_num
        asset_dict['cat_list'] = asset.cat_list
        assets_serialized.append(asset_dict)

    # Return JSON response
    return JsonResponse(assets_serialized, safe=False)

@api_view(['GET'])
def list_asset_groups_api(request):
    asset_groups = []
    for asset_group in AssetGroup.objects.all():
        ag = asset_group.to_dict()
        # Extract asset names to display
        asset_list = [asset.value for asset in asset_group.assets.all()]
        ag["assets_names"] = ", ".join(asset_list)
        ag["risk_grade"] = asset_group.get_risk_grade()
        asset_groups.append(ag)
    
    return JsonResponse(asset_groups, safe=False)
    
    
@api_view(['GET'])
def billing_assets_api(request):
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
def refresh_all_asset_grade_api(request):
    for asset in Asset.objects.all():
        asset.calc_risk_grade()
    for assetgroup in AssetGroup.objects.all():
        assetgroup.calc_risk_grade()
    return redirect('list_assets_view')


@api_view(['GET'])
def refresh_asset_grade_api(request, asset_id=None):
    if asset_id:
        asset = get_object_or_404(Asset, id=asset_id)
        asset.calc_risk_grade()
    else:
        # update all
        for asset in Asset.objects.all():
            asset.calc_risk_grade()
    return redirect('list_assets_view')


@api_view(['GET'])
def list_asset_owners(request):
    owners = []
    for owner in AssetOwner.objects.all():
        tmp_owner = owner.to_dict()
        tmp_owner["nb_assets"] = owner.assets.all().count()
        tmp_owner["nb_contacts"] = owner.contacts.all().count()
        tmp_owner["nb_documents"] = owner.documents.all().count()
        owners.append(tmp_owner)
        return JsonResponse(owners, safe=False)



@api_view(['GET'])
def refresh_assetgroup_grade_api(request, assetgroup_id=None):
    if assetgroup_id:
        assetgroup = get_object_or_404(AssetGroup, id=assetgroup_id)
        assetgroup_id.calc_risk_grade()
    else:
        # update all
        for assetgroup in AssetGroup.objects.all():
            assetgroup.calc_risk_grade()
    return JsonResponse({"status": "success"}, safe=False)

# modificação risco quantitativo - "value_fin
@api_view(['GET'])
def export_assets_api(request, assetgroup_id=None):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="pinegap_assets.csv"'
    writer = csv.writer(response, delimiter=';')

    assets = []
    if assetgroup_id:
        asset_group = AssetGroup.objects.get(id=assetgroup_id)
        for asset in asset_group.assets.all():
            assets.append(asset)
    else:
        # assets = Asset.objects.filter(owner_id=request.user.id)
        assets = Asset.objects.all()

    writer.writerow(['Endereco_do_Ativo', 'Nome_do_Ativo', 'Tipo_do_Ativo', 'Descricao_do_Ativo', 'Criticidade_do_Ativo', 'Valor_em_Risco', 'Categoria_do_Ativo'])
    for asset in assets:
        writer.writerow([smart_str(asset.value), asset.name, asset.type, smart_str(asset.description), asset.criticity, asset.financeiro,  ",".join([a.value for a in asset.categories.all()])])
    return response



@api_view(['GET'])
def export_assetgroups_api(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="assetgroups_export.csv"'
    writer = csv.writer(response, delimiter=';')

    writer.writerow([
        'Endereco_do_Ativo', 'Nome_do_Ativo', 'Tipo_do_Ativo', 'Descricao',
        'Criticidade_do_Ativo','Valor_em_Risco', 'Grupo_do_Ativo', 'Categoria_do_Ativo'])

    for assetgroup in AssetGroup.objects.all().order_by('name'):
        for asset in assetgroup.assets.all():
            try:
                asset_owner = asset.owner.username
            except Exception:
                asset_owner = ""

            writer.writerow([
                smart_str(asset.value),
                asset.name,
                asset.type,
                smart_str(asset.description),
                asset.criticity,
                asset.financeiro,
                smart_str(assetgroup.name),
                ",".join([a.value for a in asset.categories.all()]),
            ])
    return response



@api_view(['PUT'])
def add_asset_api(request):
    new_asset_args = QueryDict(request.body)
    tags = new_asset_args.getlist('tags')
    new_asset_args_dict = QueryDict(request.body).dict()
    new_asset_args_dict.update({"owner": request.user})
    new_asset_args_dict.pop("tags", None)

    asset = Asset(**new_asset_args_dict)
    asset.save()

    # Add categories
    for cat in tags:
        c = AssetCategory.objects.filter(value=cat).first()
        if c:
            asset.categories.add(c)
    asset.save()

    return JsonResponse(asset.to_dict())

@api_view(['POST'])
def update_criticity_assets_api(request):
    data = request.data
    assets = data['assets']
    criticity = data['criticity']
    if any(criticity in d for d in ASSET_CRITICITIES):
        a.set_criticity(criticity)

    return JsonResponse({'status': 'success'})


@api_view(['POST'])
def delete_assets_api(request):
    assets = request.data
    for asset_id in assets:
        a = Asset.objects.get(id=asset_id)
        a.delete()

    return JsonResponse({'status': 'success'})


@api_view(['POST', 'DELETE'])
def delete_asset_api(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)
    asset.delete()

    return JsonResponse({'status': 'success'})


@api_view(['POST'])
def delete_assetgroup_api(request, assetgroup_id):
    assetgroup = get_object_or_404(AssetGroup, id=assetgroup_id)
    assetgroup.delete()

    return JsonResponse({'status': 'success'}, json_dumps_params={'indent': 2})


@api_view(['GET'])
def get_asset_tags_api(request):
    tags = AssetCategory.objects.values_list('value', flat=True)
    return JsonResponse(list(tags), safe=False)


def _add_asset_tags(asset, new_value):
    new_tag = AssetCategory.objects.filter(value__iexact=new_value).first()
    if not new_tag:
        if not AssetCategory.objects.filter(value="Custom").first():
            AssetCategory.objects.create(value="Custom", comments="custom tags")
        custom_tags = AssetCategory.objects.get(value="Custom")
        new_tag = custom_tags.add_child(value=new_value)

        Event.objects.create(message="[AssetCategory/add_asset_tags()] New AssetCategory created: '{}' with id: {}.".format(new_value, new_tag.id),
                     type="INFO", severity="INFO")

    if new_tag not in asset.categories.all():  # Not already set
        # Check if futures parents has been already selected. If True: delete them
        cats = list(asset.categories.all().values_list('value', flat=True))
        if new_tag.get_all_parents():
            pars = [t.value for t in new_tag.get_all_parents()]
        else:
            pars = []
        intersec_par = set(pars).intersection(cats)
        if intersec_par:
            asset.categories.remove(AssetCategory.objects.get(value=list(intersec_par)[0]))

        # Check if current tags are not children of the new tag.
        # If True: delete them
        chis = [t.value for t in new_tag.get_children()]
        for c in set(chis).intersection(cats):
            asset.categories.remove(AssetCategory.objects.get(value=c))

    return new_tag


@api_view(['POST'])
def add_asset_tags_api(request, asset_id):
    if request.method == 'POST':
        asset = get_object_or_404(Asset, id=asset_id)
        new_tag = _add_asset_tags(asset, request.POST.getlist('input-search-tags')[0])
        asset.categories.add(new_tag)
        asset.save()

    return redirect('detail_asset_view', asset_id=asset_id)


@api_view(['POST'])
def add_asset_group_tags_api(request, assetgroup_id):
    if request.method == 'POST':
        asset_group = get_object_or_404(AssetGroup, id=assetgroup_id)
        new_tag = _add_asset_tags(asset_group, request.POST.getlist('input-search-tags')[0])
        asset_group.categories.add(new_tag)

    return redirect('detail_asset_group_view', assetgroup_id=assetgroup_id)


@api_view(['POST'])
def delete_asset_tags_api(request, asset_id):
    tag_id = request.POST.get('tag_id', None)
    try:
        tag = AssetCategory.objects.get(id=tag_id)
    except AssetCategory.DoesNotExist:
        Event.objects.create(message="[AssetCategory/delete_asset_tags_api()] Asset with id '{}' was not found.".format(asset_id),
                     type="ERROR", severity="ERROR")
        return redirect('detail_asset_view', asset_id=asset_id)

    if request.method == 'POST':
        asset = get_object_or_404(Asset, id=asset_id)
        asset.categories.remove(tag)  # @todo: check error cases

    return redirect('detail_asset_view', asset_id=asset_id)


@api_view(['POST'])
def delete_asset_group_tags_api(request, assetgroup_id):
    tag_id = request.POST.get('tag_id', None)
    try:
        tag = AssetCategory.objects.get(id=tag_id)
    except AssetCategory.DoesNotExist:
        Event.objects.create(message="[AssetCategory/delete_asset_group_tags_api()] AssetGroup with id '{}' was not found.".format(assetgroup_id),
                     type="ERROR", severity="ERROR")
        return redirect('detail_asset_group_view', assetgroup_id=assetgroup_id)

    if request.method == 'POST':
        assetgroup = get_object_or_404(AssetGroup, id=assetgroup_id)
        assetgroup.categories.remove(tag)  # @todo: check error cases

    return redirect('detail_asset_group_view', assetgroup_id=assetgroup_id)


@api_view(['GET'])
def get_asset_report_html_api(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)

    # Score - modificado
    #response = model_to_dict(asset, fields=[field.name for field in asset._meta.fields])

    findings_tmp = list()
    findings_stats = {}

    # @todo: invert loops
    for sev in ["critical", "high", "medium", "low", "info"]:
        tmp = Finding.objects.filter(asset=asset.id, severity=sev).order_by('type')
        if tmp.count() > 0:
            findings_tmp += tmp
        findings_stats.update({sev: tmp.count()})
    findings_stats.update({"total": len(findings_tmp)})

    return render(request, 'report-asset-findings.html', {
        'asset': asset,
        'findings': findings_tmp,
        'findings_stats': findings_stats})


@api_view(['GET'])
def get_asset_carta_html_api(request, asset_id):
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

    return render(request, 'report-asset-findings-accept.html', {
        'asset': asset,
        'findings': findings_tmp,
        'findings_stats': findings_stats})

@api_view(['GET'])
def get_asset_sumarizado_html_api(request, asset_id):
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

    return render(request, 'report-asset-findings-summary.html', {
        'asset': asset,
        'findings': findings_tmp,
        'findings_stats': findings_stats})

@api_view(['GET'])
def get_asset_billing_html_api(request, asset_id):
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


@api_view(['GET'])
def get_asset_report_json_api(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)

    findings_tmp = list()
    findings_stats = {}

    # @todo: invert loops
    for sev in ["critical", "high", "medium", "low", "info"]:
        tmp = Finding.objects.filter(asset=asset.id, severity=sev).order_by('type')
        findings_stats.update({sev: tmp.count()})
        if tmp.count() > 0:
        #    findings_tmp += tmp
        #findings_stats.update({sev: tmp.count()})
    #findings_stats.update({"total": len(findings_tmp)})  # Alter to Report
            for f in tmp:
                tmp_f = model_to_dict(f, exclude=["scopes"])
                tmp_f.update({"scopes": [ff.name for ff in f.scopes.all()]})
                findings_tmp.append(tmp_f)

    asset_dict = model_to_dict(asset, exclude=["categories"])
    asset_dict.update({"categories": [tag.value for tag in asset.categories.all()]})

    return JsonResponse({
        'asset': asset_dict,
        'findings': findings_tmp,
        'findings_stats': findings_stats
        }, safe=False)


@api_view(['GET'])
def get_asset_group_report_html_api(request, asset_group_id):
    asset_group = get_object_or_404(AssetGroup, id=asset_group_id)

    for asset in asset_group.assets.all():
        findings_tmp = list()
        findings_stats = {}

        # @todo: invert loops
        for sev in ["critical", "high", "medium", "low", "info", "total"]:
            tmp = Finding.objects.filter(asset=asset.id, severity=sev).order_by('type')
            findings_stats.update({sev: tmp.count()})
            if tmp.count() > 0:
       #         findings_tmp += tmp
       #     findings_stats.update({sev: tmp.count()})
       # findings_stats.update({"total": len(findings_tmp)})   #alter to report
                for f in tmp:
                    tmp_f = model_to_dict(f, exclude=["scopes"])
                    tmp_f.update({"scopes": [ff.name for ff in f.scopes.all()]})
                    findings_tmp.append(tmp_f)

        asset_dict = model_to_dict(asset, exclude=["categories"])
        asset_tags = [tag.value for tag in asset.categories.all()]
        asset_dict.update({"categories": asset_tags})

    return render(request, 'report-assetgroup-findings.html', {
        'asset_group': asset_group,
        'findings': findings_tmp,
        'findings_stats': findings_stats})


@api_view(['GET'])
def get_asset_group_report_json_api(request, asset_group_id):
    asset_group = get_object_or_404(AssetGroup, id=asset_group_id)

    assets = list()
    for asset in asset_group.assets.all():

        findings_tmp = list()
        findings_stats = {}

        # @todo: invert loops
        for sev in ["critical", "high", "medium", "low", "info", "total"]:
            tmp = Finding.objects.filter(asset=asset.id, severity=sev).order_by('type')
            findings_stats.update({sev: tmp.count()})
            if tmp.count() > 0:
                for f in tmp:
                    tmp_f = model_to_dict(f, exclude=["scopes"])
                    tmp_f.update({"scopes": [ff.name for ff in f.scopes.all()]})
                    findings_tmp.append(tmp_f)

        asset_dict = model_to_dict(asset, exclude=["categories"])
        asset_tags = [tag.value for tag in asset.categories.all()]
        asset_dict.update({"categories": asset_tags})
        assets.append({
            'asset': asset_dict,
            'findings': findings_tmp,
            'findings_stats': findings_stats
            })

    return JsonResponse(assets, safe=False)


@api_view(['GET'])
def get_asset_owner_doc_api(request, asset_owner_doc_id):
    doc = get_object_or_404(AssetOwnerDocument, id=asset_owner_doc_id)
    fp = urllib.unquote(doc.filepath)
    fn = urllib.unquote(doc.filename)

    file_wrapper = FileWrapper(file(fp, 'rb'))
    file_mimetype = mimetypes.guess_type(fp)
    response = HttpResponse(file_wrapper, content_type=file_mimetype)
    response['X-Sendfile'] = fp
    response['Content-Length'] = os.stat(fp).st_size
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(fn)
    return response


@api_view(['POST'])
def edit_asset_owner_comments_api(request, asset_owner_id):
    if request.method != "POST" or not request.POST.get('new_comments', None):
        return HttpResponse(status=400)

    owner = get_object_or_404(AssetOwner, id=asset_owner_id)
    owner.comments = request.POST.get('new_comments')
    owner.save()
    return HttpResponse(status=200)


@api_view(['POST'])
def delete_asset_owner_contact_api(request, asset_owner_id):
    # if request.method != 'POST':
    #     return HttpResponse(status=400)

    contact = get_object_or_404(AssetOwnerContact, id=asset_owner_id)
    contact.delete()
    return redirect('details_asset_owner_view', asset_owner_id=asset_owner_id)


@api_view(['POST'])
def delete_asset_owner_document_api(request, asset_owner_id):
    if request.method != 'POST' or not request.POST.get('doc_id', None):
        return HttpResponse(status=400)

    doc_id = request.POST.get('doc_id')
    document = get_object_or_404(AssetOwnerDocument, id=doc_id)
    document.delete()
    return redirect('details_asset_owner_view', asset_owner_id=asset_owner_id)


@api_view(['POST'])
def add_asset_owner_document_api(request, asset_owner_id):
    owner = get_object_or_404(AssetOwner, id=asset_owner_id)
    form = AssetOwnerDocumentForm(request.POST, request.FILES)
    if form.is_valid():
        doc_args = {
            'doctitle': form.cleaned_data['doctitle'],
            'tlp_color': form.cleaned_data['tlp_color'],
            'comments': form.cleaned_data['comments'],
            'owner': request.user,
        }
        if request.FILES:
            # Create /media/ folders if not exists
            if not os.path.exists(MEDIA_ROOT+"/owners_docs"):
                os.makedirs(MEDIA_ROOT+"/owners_docs")
            if not os.path.exists(MEDIA_ROOT+"/owners_docs/"+str(request.user.id)):
                os.makedirs(MEDIA_ROOT+"/owners_docs/"+str(request.user.id))

            myfile = request.FILES['file']
            fs = FileSystemStorage(location=MEDIA_ROOT+"/owners_docs/"+str(request.user.id), base_url=MEDIA_ROOT+"/owners_docs/"+str(request.user.id))
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            doc_args.update({
                'filename': filename,
                'filepath': uploaded_file_url
            })

        doc = AssetOwnerDocument(**doc_args)
        doc.save()

        # Add this document to the asset owner
        owner.documents.add(doc)
        owner.save()

    return redirect('details_asset_owner_view', asset_owner_id=asset_owner_id)


@api_view(['POST'])
def add_asset_owner_contact_api(request, asset_owner_id):
    owner = get_object_or_404(AssetOwner, id=asset_owner_id)

    form = AssetOwnerContactForm(request.POST)
    if form.is_valid():
        contact_args = {
            'name': form.cleaned_data['name'],
            'title': form.cleaned_data['title'],
            'email': form.cleaned_data['email'],
            'phone': form.cleaned_data['phone'],
            'address': form.cleaned_data['address'],
            'url': form.cleaned_data['url'],
            'comments': form.cleaned_data['comments'],
            'owner': request.user,
        }

        contact = AssetOwnerContact(**contact_args)
        contact.save()

        # Add this contact to the asset owner
        owner.contacts.add(contact)
        owner.save()

    return redirect('details_asset_owner_view', asset_owner_id=asset_owner_id)


