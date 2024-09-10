# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Value, CharField, Case, When, Q, F, Count
from django.utils import timezone as tz
from whitelabels.models import Brand
from django.db.models.functions import Lower #
from .apis import _add_asset_tags #
from .apis import export_assetgroups_api #

# Implement Control Access of Url - By BILL
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404

###################################

from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.postgres.aggregates import ArrayAgg
from django.shortcuts import render, redirect, get_object_or_404

from .forms import AssetForm, AssetGroupForm, AssetBulkForm, AssetOwnerForm
from .models import Asset, AssetGroup, AssetOwner, AssetCategory
from .models import ASSET_INVESTIGATION_LINKS
from findings.models import Finding
from engines.models import EnginePolicyScope
from scans.models import Scan, ScanDefinition
from common.utils import encoding

from datetime import timedelta, datetime
from pytz import timezone
import csv
import copy


# Modificacao para adicionar risco quantitativo - "financeiro"
def list_assets_view(request):
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

    # List asset groups
    asset_groups = []
    for asset_group in AssetGroup.objects.all():
        ag = model_to_dict(asset_group)
        # extract asset names to diplay
        asset_list = []
        for asset in asset_group.assets.all():
            asset_list.append(asset.value)

        ag["assets_names"] = ", ".join(asset_list)
        ag["risk_grade"] = asset_group.get_risk_grade()
        asset_groups.append(ag)



# Modificado - novo algoritimo de classificacao de risco
    return render(request, 'list-assets.html', {
        'assets': assets,
        'asset_groups': asset_groups
})


# modificação adicionar risco quantitativo -  'financeiro' - By BILL
# Add Bloqueio de URL - By BILL
@user_passes_test(lambda u: u.groups.filter(name='visitante').count() == 0, login_url='/assets/deny/')
@user_passes_test(lambda u: u.groups.filter(name='analista').count() == 0,  login_url='/assets/deny/')
@user_passes_test(lambda u: u.groups.filter(name='dpo').count() == 0, login_url='/assets/deny/')
def add_asset_view(request):
    form = None

    if request.method == 'GET':
        form = AssetForm()
    elif request.method == 'POST':
        form = AssetForm(request.POST)
        if form.is_valid():
            asset_args = {
                'value': encoding.unicode_escape(form.cleaned_data['value']),
                'name': form.cleaned_data['name'],
                'type': form.cleaned_data['type'],
                'criticity': form.cleaned_data['criticity'],
                'financeiro': form.cleaned_data['financeiro'],
                'description': form.cleaned_data['description'],
                'owner': request.user,
            }
            asset = Asset(**asset_args)
            asset.save()

            # Add categories - modificado eliminar erro de add asset

            if form.data.getlist('categories'):
                asset.categories.clear()
                for cat_id in form.data.getlist('categories'):
                    asset.categories.add(AssetCategory.objects.get(id=cat_id))
            asset.save()

            if asset.type in ['ip-range', 'ip-subnet']:
                # Create an asset group dynamically
                assetgroup_args = {
                    'name': "{} assets".format(asset.name),
                    'criticity': asset.criticity,
                    'description': "Ativo criado dinamicamente. Imported desc: {}".format(asset.description),
                    'owner': request.user
                }
                asset_group = AssetGroup(**assetgroup_args)
                asset_group.save()

                # Add the asset to the new group
                asset_group.assets.add(asset)
                asset_group.save()

                # Caculate the risk grade
                asset_group.calc_risk_grade()
                asset_group.save()


            messages.success(request, 'Ativo criado com sucesso')
            return redirect('list_assets_view')



    return render(request, 'add-asset.html', {'form': form})

# Modificação - Risco quantitativo - "financeiro"
# Add Bloqueio de URL - By BILL
@user_passes_test(lambda u: u.groups.filter(name='visitante').count() == 0, login_url='/assets/deny/')
@user_passes_test(lambda u: u.groups.filter(name='analista').count() == 0,  login_url='/assets/deny/')
@user_passes_test(lambda u: u.groups.filter(name='dpo').count() == 0, login_url='/assets/deny/')
def edit_asset_view(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)

    form = AssetForm()
    if request.method == 'GET':
        form = AssetForm(instance=asset)
    elif request.method == 'POST':
        form = AssetForm(request.POST, instance=asset)
        if form.is_valid():
            asset.value = form.cleaned_data['value'].encode('utf-8')
            asset.name = form.cleaned_data['name']
            asset.type = form.cleaned_data['type']
            asset.description = form.cleaned_data['description']
            asset.financeiro = form.cleaned_data['financeiro']
            asset.criticity = form.cleaned_data['criticity']
            asset.evaluate_risk()

            if form.data.getlist('categories'):
                asset.categories.clear()
                for cat_id in form.data.getlist('categories'):
                    asset.categories.add(AssetCategory.objects.get(id=cat_id))
            asset.save()

            messages.success(request, 'Ativo aualizado com sucesso')
            return redirect('list_assets_view')

    return render(request, 'edit-asset.html', {'form': form, 'asset': asset})

# Add Bloqueio de URL - By BILL
@user_passes_test(lambda u: u.groups.filter(name='visitante').count() == 0, login_url='/assets/deny/')
@user_passes_test(lambda u: u.groups.filter(name='analista').count() == 0,  login_url='/assets/deny/')
@user_passes_test(lambda u: u.groups.filter(name='dpo').count() == 0, login_url='/assets/deny/')
def add_asset_group_view(request):
    form = None

    if request.method == 'GET':
        form = AssetGroupForm()
    elif request.method == 'POST':
        form = AssetGroupForm(request.POST)
        if form.is_valid():
            asset_args = {
                'name': form.cleaned_data['name'],
                'criticity': form.cleaned_data['criticity'],
                'description': form.cleaned_data['description'],
                'owner': request.user
            }
            asset_group = AssetGroup(**asset_args)
            asset_group.save()

            for asset_id in form.data.getlist('assets'):
                asset_group.assets.add(Asset.objects.get(id=asset_id))
            asset_group.save()

            # Add categories
            for cat in form.data['categories']:
                asset_group.categories.add(cat)
            asset_group.save()

            asset_group.calc_risk_grade()
            asset_group.save()
            messages.success(request, 'Grupo criado com sucesso')

            return redirect('list_assets_view')
    return render(request, 'add-asset-group.html', {'form': form})


# Add Bloqueio de URL - By BILL
@user_passes_test(lambda u: u.groups.filter(name='visitante').count() == 0, login_url='/assets/deny/')
@user_passes_test(lambda u: u.groups.filter(name='analista').count() == 0,  login_url='/assets/deny/')
@user_passes_test(lambda u: u.groups.filter(name='dpo').count() == 0, login_url='/assets/deny/')
def edit_asset_group_view(request, assetgroup_id):
    asset_group = get_object_or_404(AssetGroup, id=assetgroup_id)

    form = AssetGroupForm()
    if request.method == 'GET':
        form = AssetGroupForm(instance=asset_group)
    elif request.method == 'POST':
        # form = AssetGroupForm(request.POST)
        form = AssetGroupForm(request.POST, instance=asset_group)
        if form.is_valid():
            if asset_group.name != form.cleaned_data['name']:
                asset_group.name = form.cleaned_data['name']
            asset_group.description = form.cleaned_data['description']
            asset_group.criticity = form.cleaned_data['criticity']
            asset_group.assets.clear()
            for asset_id in form.data.getlist('assets'):
                asset_group.assets.add(Asset.objects.get(id=asset_id))
            asset_group.evaluate_risk()
            asset_group.save()

            asset_group.calc_risk_grade()
            asset_group.save()

            messages.success(request, 'Grupo atualizado com sucesso')
            return redirect('list_assets_view')

    return render(request, 'edit-asset-group.html', {
        'form': form,
        'assetgroup_id': assetgroup_id,
        'asset_group': asset_group
    })



# New Import Approach - By BILL
# Add Bloqueio de URL - By BILL
@user_passes_test(lambda u: u.groups.filter(name='visitante').count() == 0, login_url='/assets/deny/')
@user_passes_test(lambda u: u.groups.filter(name='analista').count() == 0,  login_url='/assets/deny/')
@user_passes_test(lambda u: u.groups.filter(name='dpo').count() == 0, login_url='/assets/deny/')
def bulkadd_asset_view(request):
    form = None

    if request.method == 'GET':
        form = AssetBulkForm()
    elif request.method == 'POST':
        form = AssetBulkForm(request.POST, request.FILES)
        if request.FILES:
            records = csv.reader(request.FILES['file'], delimiter=str(u';').encode('utf-8'), quotechar=str(u'"').encode('utf-8'))
            records.next()

            for line in records:
		# Add Assets
                if Asset.objects.filter(value=line[0]).count() > 0:
                    continue

		asset_args = {
                    'value': line[0],
                    'name': line[1],
                    'type': line[2],
                    'description': line[3],
                    'criticity': line [4],
                    'financeiro': line [5],
                    'owner': User.objects.get(id=request.user.id),
                    'status': "new",
                        }

                asset = Asset(**asset_args)
                asset.save()

                # Add groups
                if len(line) >= 5 and line[6] != "":
                    ag = AssetGroup.objects.filter(name=str(line[6])).first()
                    if ag is None:  # Create new asset group
                        asset_args = {
                            'name': line[6],
                            'criticity': "low",
                            'description': "Importado e criado automaticamente.",
                            'owner': request.user
                        }
                        ag = AssetGroup(**asset_args)
                        ag.save()
		    # add the asset to the group
 		    ag.assets.add(asset)

                # Manage tags (categories)
                if len(line) >= 6 and line[7] != "":
                    for tag in line[7].split(","):
                        new_tag = _add_asset_tags(asset, tag)
                        asset.categories.add(new_tag)
                        asset.save()

	messages.success(request, 'Importado e criado com sucesso')
	return redirect('list_assets_view')
    return render(request, 'add-assets-bulk.html', {'form': form })





# todo: change to asset_id
def evaluate_asset_risk_view(request, asset_name):
    asset = get_object_or_404(Asset, value=asset_name)
    data = asset.evaluate_risk()
    return JsonResponse(data, safe=False)


def detail_asset_view(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)
    findings = Finding.objects.filter(asset=asset).annotate(
        severity_numm=Case(
            When(severity="critical", then=Value("0")),
            When(severity="high", then=Value("1")),
            When(severity="medium", then=Value("2")),
            When(severity="low", then=Value("3")),
            When(severity="info", then=Value("4")),
            default=Value("1"),
            output_field=CharField())
        ).annotate(
            scope_list=ArrayAgg('scopes__name')
        ).order_by('severity_numm', 'type', 'updated_at', 'found_at', 'created_at')

    findings_stats = {'total': 0, 'critical': 0, 'high': 0, 'medium': 0, 'low': 0, 'info': 0, 'new': 0, 'ack': 0, 'patched': 0, 'false-positive': 0, 'mitigated': 0, 'confirmed': 0, 'closed': 0, 'cvss_gte_7': 0, 'created_at': 0, 'found_at': 0}
    engines_stats = {}
    references = {}

    engine_scopes = {}
    for engine_scope in EnginePolicyScope.objects.all():
        engine_scopes.update({
            engine_scope.name: {
                'priority': engine_scope.priority,
                'id': engine_scope.id,
                'total': 0,
                'critical': 0,
                'high': 0,
                'medium': 0,
                'low': 0,
                'info': 0
            }
        })

    for finding in findings:
        findings_stats['total'] = findings_stats.get('total', 0) + 1
        findings_stats[finding.severity] = findings_stats.get(finding.severity, 0) + 1
        if finding.status == 'new':
            findings_stats['new'] = findings_stats.get('new', 0) + 1
        if finding.status == 'ack':
            findings_stats['ack'] = findings_stats.get('ack', 0) + 1
        if finding.status == 'patched':
            findings_stats['patched'] = findings_stats.get('patched', 0) + 1
        if finding.status == 'false-positive':
            findings_stats['false-positive'] = findings_stats.get('false-positive', 0) + 1
        if finding.status == 'mitigated':
            findings_stats['mitigated'] = findings_stats.get('mitigated', 0) + 1
        if finding.status == 'confirmed':
            findings_stats['confirmed'] = findings_stats.get('confirmed', 0) + 1
        if finding.status == 'closed':
            findings_stats['closed'] = findings_stats.get('closed', 0) + 1
        for fs in finding.scope_list:
            if fs is not None:
                c = engine_scopes[fs]
                engine_scopes[fs].update({
                    'total': c['total']+1,
                    finding.severity: c[finding.severity]+1
                })
        if finding.engine_type not in engines_stats.keys():
            engines_stats.update({finding.engine_type: 0})
        engines_stats[finding.engine_type] = engines_stats.get(finding.engine_type, 0) + 1
        if finding.risk_info["cvss_base_score"] > 7.0:
            findings_stats['cvss_gte_7'] = findings_stats.get('cvss_gte_7', 0) + 1

        if bool(finding.vuln_refs):
            for ref in finding.vuln_refs.keys():
                if ref not in references.keys():
                    references.update({ref: []})
                tref = references[ref]
                if type(finding.vuln_refs[ref]) is list:
                    tref = tref + finding.vuln_refs[ref]
                else:
                    tref.append(finding.vuln_refs[ref])
                # references.update({ref: list(set(tref))})

                references.update({ref: tref})

    # Show only unique references
    references_cleaned = {}
    for ref in references:
        references_cleaned.update({ref: sorted(list(set(references[ref])))})

    # Related scans
    scans_stats = {
        'performed': Scan.objects.filter(assets__in=[asset]).count(),
        'defined': ScanDefinition.objects.filter(assets_list__in=[asset]).count(),
        'periodic': ScanDefinition.objects.filter(assets_list__in=[asset], scan_type='periodic').count(),
        'ondemand': ScanDefinition.objects.filter(assets_list__in=[asset], scan_type='single').count(),
        'running': Scan.objects.filter(assets__in=[asset], status='started').count(),  # bug: a regrouper par assets
        'lasts': Scan.objects.filter(assets__in=[asset]).order_by('-created_at')[:3]
    }

    asset_groups = list(AssetGroup.objects.filter(assets__in=[asset]).only("id"))
    scan_defs = ScanDefinition.objects.filter(Q(assets_list__in=[asset]) | Q(assetgroups_list__in=asset_groups)).annotate(engine_type_name=F('engine_type__name')).annotate(scan_set_count=Count('scan'))
    scans = Scan.objects.filter(assets__in=[asset]).values("id", "title", "status", "summary", "updated_at", "started_at", "finished_at").annotate(engine_type_name=F('engine_type__name'))

    # Investigation links
    investigation_links = []
    DEFAULT_LINKS = copy.deepcopy(ASSET_INVESTIGATION_LINKS)
    for i in DEFAULT_LINKS:
        if asset.type in i["datatypes"]:
            i["link"] = i["link"].replace("%asset%", asset.value)
            investigation_links.append(i)

    # Calculate automatically risk grade
    asset.calc_risk_grade()
    asset_risk_grade = {
        'now': asset.get_risk_grade(),
        'day_ago': asset.get_risk_grade(history=1),
        'week_ago': asset.get_risk_grade(history=7),
        'month_ago': asset.get_risk_grade(history=30),
        '2m_ago': asset.get_risk_grade(history=60),
        '3m_ago': asset.get_risk_grade(history=90),
        '4m_ago': asset.get_risk_grade(history=120),
        '5m_ago': asset.get_risk_grade(history=150),
        '6m_ago': asset.get_risk_grade(history=180),
        'year_ago': asset.get_risk_grade(history=365)
    }


    return render(request, 'details-asset.html', {
        'asset': asset,
        'asset_risk_grade': asset_risk_grade,
        'findings': findings,
        'findings_stats': findings_stats,
        'references': references_cleaned,
        'scans_stats': scans_stats,
        'scans': scans,
        'scan_defs': scan_defs,
        'investigation_links': investigation_links,
        'engines_stats': engines_stats,
        'asset_scopes': sorted(engine_scopes.iteritems(), key=lambda (x, y): y['priority'])
        })



def detail_asset_group_view(request, assetgroup_id):
    asset_group = get_object_or_404(AssetGroup, id=assetgroup_id)
    assets = asset_group.assets.all()
    findings = Finding.objects.filter(asset__in=assets).annotate(severity_numm=Case(
            When(severity="critical", then=Value("0")),
            When(severity="high", then=Value("1")),
            When(severity="medium", then=Value("2")),
            When(severity="low", then=Value("3")),
            When(severity="info", then=Value("4")),
            default=Value("1"),
            output_field=CharField())).annotate(scope_list=ArrayAgg('scopes__name')).order_by('asset', 'severity_numm', 'type', 'updated_at')

    asset_scopes = {}
    for scope in EnginePolicyScope.objects.all():
        asset_scopes.update({
            scope.name: {
                'priority': scope.priority,
                'id': scope.id,
                'total': 0,
                'critical': 0,
                'high': 0,
                'medium': 0,
                'low': 0,
                'info': 0
            }
        })

    findings_stats = {'total': 0, 'critical': 0, 'high': 0, 'medium': 0, 'low': 0, 'info': 0, 'new': 0, 'ack': 0, 'patched': 0, 'false-positive': 0, 'mitigated': 0, 'confirmed': 0, 'closed': 0}
    engines_stats = {}

    for finding in findings:
        findings_stats['total'] = findings_stats.get('total', 0) + 1
        findings_stats[finding.severity] = findings_stats.get(finding.severity, 0) + 1
        if finding.status == 'new':
            findings_stats['new'] = findings_stats.get('new', 0) + 1
        if finding.status == 'ack':
            findings_stats['ack'] = findings_stats.get('ack', 0) + 1
        if finding.status == 'patched':
            findings_stats['patched'] = findings_stats.get('patched', 0) + 1
        if finding.status == 'false-positive':
            findings_stats['false-positive'] = findings_stats.get('false-positive', 0) + 1
        if finding.status == 'mitigated':
            findings_stats['mitigated'] = findings_stats.get('mitigated', 0) + 1
        if finding.status == 'confirmed':
            findings_stats['confirmed'] = findings_stats.get('confirmed', 0) + 1
        if finding.status == 'closed':
            findings_stats['closed'] = findings_stats.get('closed', 0) + 1

        for fs in finding.scope_list:
            if fs is not None:
                c = asset_scopes[fs]
                asset_scopes[fs].update({'total': c['total']+1, finding.severity: c[finding.severity]+1})

        if finding.engine_type not in engines_stats.keys():
            engines_stats.update({finding.engine_type: 0})
        engines_stats[finding.engine_type] = engines_stats.get(finding.engine_type, 0) + 1

    # Scans
    scan_defs = ScanDefinition.objects.filter(Q(assetgroups_list__in=[asset_group])).annotate(engine_type_name=F('engine_type__name'))
    scans = []
    for scan_def in scan_defs:
        scans = scans + list(scan_def.scan_set.all())

    scans_stats = {
        'performed': len(scans),
        'defined': len(scan_defs),
        'periodic': scan_defs.filter(scan_type='periodic').count(),
        'ondemand': scan_defs.filter(scan_type='single').count(),
        'running': scan_defs.filter(status='started').count() #bug: a regrouper par assets
    }

    # calculate automatically risk grade
    # asset_group.calc_risk_grade()
    asset_group_risk_grade = {
        'now': asset_group.get_risk_grade(),
        # 'day_ago': asset_group.get_risk_grade(history = 1),
        # 'week_ago': asset_group.get_risk_grade(history = 7),
        # 'month_ago': asset_group.get_risk_grade(history = 30),
        # 'year_ago': asset_group.get_risk_grade(history = 365)
    }

    return render(request, 'details-asset-group.html', {
        'asset_group': asset_group,
        'asset_group_risk_grade': asset_group_risk_grade,
        'assets': assets,
        'findings': findings,
        'findings_stats': findings_stats,
        'scans_stats': scans_stats,
        'scans': scans,
        'scan_defs': scan_defs,
        'engines_stats': engines_stats,
        'asset_scopes': sorted(asset_scopes.iteritems(), key=lambda (x, y): y['priority'])
    })


# Asset Owners
def list_asset_owners_view(request):
    owners = []
    for owner in AssetOwner.objects.all():
        tmp_owner = model_to_dict(owner)
        tmp_owner["nb_assets"] = owner.assets.all().count()
        tmp_owner["nb_contacts"] = owner.contacts.all().count()
        tmp_owner["nb_documents"] = owner.documents.all().count()
        owners.append(tmp_owner)

    return render(request, 'list-asset-owners.html', {'owners': owners})


# Add Bloqueio de URL - By BILL
@user_passes_test(lambda u: u.groups.filter(name='visitante').count() == 0, login_url='/assets/deny/')
@user_passes_test(lambda u: u.groups.filter(name='analista').count() == 0,  login_url='/assets/deny/')
@user_passes_test(lambda u: u.groups.filter(name='dpo').count() == 0, login_url='/assets/deny/')
def add_asset_owner_view(request):
    form = None
    if request.method == 'GET':
        form = AssetOwnerForm()
    elif request.method == 'POST':
        form = AssetOwnerForm(request.POST)

        if form.errors:
            print (form.errors)

        if form.is_valid():
            owner_args = {
                'name': form.cleaned_data['name'],
                'url': form.cleaned_data['url'],
                'comments': form.cleaned_data['comments'],
                'owner': request.user,
            }
            owner = AssetOwner(**owner_args)
            owner.save()
            for asset_id in form.data.getlist('assets'):
                owner.assets.add(Asset.objects.get(id=asset_id))
            owner.save()
            messages.success(request, 'Criado com sucesso')

            return redirect('list_asset_owners_view')
    return render(request, 'add-asset-owner.html', {'form': form})


# Add Bloqueio de URL - By BILL
@user_passes_test(lambda u: u.groups.filter(name='visitante').count() == 0, login_url='/assets/deny/')
@user_passes_test(lambda u: u.groups.filter(name='analista').count() == 0,  login_url='/assets/deny/')
@user_passes_test(lambda u: u.groups.filter(name='dpo').count() == 0, login_url='/assets/deny/')
def delete_asset_owner_view(request, asset_owner_id):
    if request.method == 'POST':
        owner = get_object_or_404(AssetOwner, id=asset_owner_id)
        owner.delete()
        messages.success(request, 'Excluido com sucesso!')
        return redirect('list_asset_owners_view')
    return render(request, 'delete-asset-owner.html', {'owner': owner})


def details_asset_owner_view(request, asset_owner_id):
    owner = model_to_dict(get_object_or_404(AssetOwner, id=asset_owner_id))
    return render(request, 'details-asset-owner.html', {'owner': owner})

def billing_assets_view(request):
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
    allowed_filter_fields = ["id", "name", "criticity", "financeiro", "type", "score", "created_at"]
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

    # List asset groups
    asset_groups = []
    for asset_group in AssetGroup.objects.all():
        ag = model_to_dict(asset_group)
        # extract asset names to diplay
        asset_list = []
        for asset in asset_group.assets.all():
            asset_list.append(asset.value)

        ag["assets_names"] = ", ".join(asset_list)
        ag["risk_grade"] = asset_group.get_risk_grade()
        asset_groups.append(ag)


# Modificado - novo algoritimo de classificacao de risco
    return render(request, 'report-asset-statement.html', {
        'assets': assets,
        'asset_groups': asset_groups
})


# Added to print report in HTML API

def report_asset_group_view(request, assetgroup_id):
    asset_group = get_object_or_404(AssetGroup, id=assetgroup_id)
    assets = asset_group.assets.all()
    findings = Finding.objects.filter(asset__in=assets).annotate(severity_numm=Case(
            When(severity="critical", then=Value("0")),
            When(severity="high", then=Value("1")),
            When(severity="medium", then=Value("2")),
            When(severity="low", then=Value("3")),
            When(severity="info", then=Value("4")),
            default=Value("1"),
            output_field=CharField())).annotate(scope_list=ArrayAgg('scopes__name')).order_by('asset', 'severity_numm', 'type', 'updated_at')


    asset_scopes = {}
    for scope in EnginePolicyScope.objects.all():
        asset_scopes.update({
            scope.name: {
                'priority': scope.priority,
                'id': scope.id,
                'total': 0,
                'critical': 0,
                'high': 0,
                'medium': 0,
                'low': 0,
                'info': 0
            }
        })


    findings_stats = {'total': 0, 'critical': 0, 'high': 0, 'medium': 0, 'low': 0, 'info': 0, 'new': 0, 'ack': 0, 'patched': 0, 'false-positive': 0, 'mitigated': 0, 'confirmed': 0, 'closed': 0}
    engines_stats = {}


    for finding in findings:
        findings_stats['total'] = findings_stats.get('total', 0) + 1
        findings_stats[finding.severity] = findings_stats.get(finding.severity, 0) + 1
        if finding.status == 'new':
            findings_stats['new'] = findings_stats.get('new', 0) + 1
        if finding.status == 'ack':
            findings_stats['ack'] = findings_stats.get('ack', 0) + 1
        if finding.status == 'patched':
            findings_stats['patched'] = findings_stats.get('patched', 0) + 1
        if finding.status == 'false-positive':
            findings_stats['false-positive'] = findings_stats.get('false-positive', 0) + 1
        if finding.status == 'mitigated':
            findings_stats['mitigated'] = findings_stats.get('mitigated', 0) + 1
        if finding.status == 'confirmed':
            findings_stats['confirmed'] = findings_stats.get('confirmed', 0) + 1
        if finding.status == 'closed':
            findings_stats['closed'] = findings_stats.get('closed', 0) + 1

        for fs in finding.scope_list:
            if fs is not None:
                c = asset_scopes[fs]
                asset_scopes[fs].update({'total': c['total']+1, finding.severity: c[finding.severity]+1})

        if finding.engine_type not in engines_stats.keys():
            engines_stats.update({finding.engine_type: 0})
        engines_stats[finding.engine_type] = engines_stats.get(finding.engine_type, 0) + 1


    # Scans
    scan_defs = ScanDefinition.objects.filter(Q(assetgroups_list__in=[asset_group])).annotate(engine_type_name=F('engine_type__name'))
    scans = []
    for scan_def in scan_defs:
        scans = scans + list(scan_def.scan_set.all())

    scans_stats = {
        'performed': len(scans),
        'defined': len(scan_defs),
        'periodic': scan_defs.filter(scan_type='periodic').count(),
        'ondemand': scan_defs.filter(scan_type='single').count(),
        'running': scan_defs.filter(status='started').count() #bug: a regrouper par assets
    }


    # calculate automatically risk grade
    # asset_group.calc_risk_grade()
    asset_group_risk_grade = {
        'now': asset_group.get_risk_grade(),
        # 'day_ago': asset_group.get_risk_grade(history = 1),
        # 'week_ago': asset_group.get_risk_grade(history = 7),
        # 'month_ago': asset_group.get_risk_grade(history = 30),
        # 'year_ago': asset_group.get_risk_grade(history = 365)
    }



    return render(request, 'report-assetgroup-findings.html', {
        'asset_group': asset_group,
        'asset_group_risk_grade': asset_group_risk_grade,
        'assets': assets,
        'findings': findings,
        'findings_stats': findings_stats,
        'scans_stats': scans_stats,
        'scans': scans,
        'scan_defs': scan_defs,
        'engines_stats': engines_stats,
        'asset_scopes': sorted(asset_scopes.iteritems(), key=lambda (x, y): y['priority'])
    })


