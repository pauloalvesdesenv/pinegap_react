# -*- coding: utf-8 -*-


##############################################

from django.http import JsonResponse #Billing
from django.forms.models import model_to_dict #Billing
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger #Billing
from django.db.models import Value, CharField, Case, When, Q, F, Count #Billing
from django.utils import timezone as tz #Billing
from django.contrib import messages #Billing
from django.contrib.auth.models import User #Billing
from django.shortcuts import render, redirect, get_object_or_404 #Billing
from django.contrib.sites.shortcuts import get_current_site
from common.utils import encoding #Billing

from django.shortcuts import render
from django.contrib.postgres.fields.jsonb import KeyTextTransform
from django.contrib.postgres.aggregates.general import ArrayAgg
from django.db.models import Count, Sum
from assets.models import Asset, AssetGroup, ASSET_TYPES
from findings.models import Finding
from scans.models import Scan, ScanDefinition
from engines.models import EngineInstance, EnginePolicy
from rules.models import Rule
from whitelabels.models import Brand
from settings.models import Setting


from datetime import timedelta, datetime
from pytz import timezone
import datetime
import operator
import copy
import ast


def homepage_dashboard_view(request):
    settings = Setting.objects.filter(key="url_setting")
    current_site = get_current_site(request)
    if not settings:
        domain = current_site.domain
        Setting.objects.create(key="url_setting", value=domain)
    if settings:
        if settings[0].value != current_site.domain:
            domain = current_site.domain
            setting = Setting.objects.get(pk=settings[0].id)
            setting.value = domain
            setting.save()
    findings = Finding.objects.all()
    global_stats = {
        "assets": {
            "total": Asset.objects.all().count(),
            "total_ag": AssetGroup.objects.all().count(),
            "risk_value_A": Asset.objects.filter(risk_level__grade="A").aggregate(Sum('financeiro'))['financeiro__sum'],
            "risk_value_B": Asset.objects.filter(risk_level__grade="B").aggregate(Sum('financeiro'))['financeiro__sum'],
            "risk_value_C": Asset.objects.filter(risk_level__grade="C").aggregate(Sum('financeiro'))['financeiro__sum'],
            "risk_value_D": Asset.objects.filter(risk_level__grade="D").aggregate(Sum('financeiro'))['financeiro__sum'],
            "risk_value_E": Asset.objects.filter(risk_level__grade="E").aggregate(Sum('financeiro'))['financeiro__sum'],
            "risk_value_F": Asset.objects.filter(risk_level__grade="F").aggregate(Sum('financeiro'))['financeiro__sum'],
            "risk_value_imponderavel": Asset.objects.filter(risk_level__grade="-").aggregate(Sum('financeiro'))['financeiro__sum'],
            "risk_value_total": Asset.objects.filter(risk_level__grade__in=["D", "E", "F"]).aggregate(Sum('financeiro'))['financeiro__sum'],

        },
        "asset_types": {},
        "findings": {
            "total": findings.count(),
            "new": findings.filter(status='new').count(),
            "critical": findings.filter(severity='critical').count(),
            "high": findings.filter(severity='high').count(),
            "medium": findings.filter(severity='medium').count(),
            "low": findings.filter(severity='low').count(),
            "info": findings.filter(status='info').count(),
            "confirmed": findings.filter(status='confirmed').count(),
            "mitigated": findings.filter(status='mitigated').count(),
        },
        "scans": {
            "defined": ScanDefinition.objects.all().count(),
            "performed": Scan.objects.all().count(),
            "active_periodic": ScanDefinition.objects.filter(enabled=True, scan_type='periodic').count(),
        },
        "engines": {
            "total": EngineInstance.objects.all().count(),
            "policies": EnginePolicy.objects.all().count(),
            "active": EngineInstance.objects.filter(status='READY', enabled=True).count(),
        },
        "rules": {
            "total": Rule.objects.all().count(),
            "active": Rule.objects.filter(enabled=True).count(),
            "nb_matches": 0,
        },
    }

    # update asset_types
    for at in ASSET_TYPES:
        global_stats["asset_types"].update({at[0]: Asset.objects.filter(type=at[0]).count()})

    # update nb_matches
    matches = 0
    for r in Rule.objects.all():
        matches += r.nb_matches
    global_stats["rules"].update({"nb_matches": matches})

    # Last 6 findings
    last_findings = Finding.objects.all().order_by('-id')[:6][::-1]

    # Last 6 scans
    last_scans = Scan.objects.all().order_by('-started_at')[:6]

    # Asset grades repartition and TOP 10
    asset_grades_map = {
        "A": {"high": 0, "medium": 0, "low": 0},
        "B": {"high": 0, "medium": 0, "low": 0},
        "C": {"high": 0, "medium": 0, "low": 0},
        "D": {"high": 0, "medium": 0, "low": 0},
        "E": {"high": 0, "medium": 0, "low": 0},
        "F": {"high": 0, "medium": 0, "low": 0},
        "-": {"high": 0, "medium": 0, "low": 0}
    }

    assetgroup_grades_map = copy.deepcopy(asset_grades_map)



    # Asset grades
    assets_risk_scores = {}
    for asset in Asset.objects.all():
        asset_grades_map[asset.risk_level["grade"]].update({
            asset.criticity: asset_grades_map[asset.risk_level["grade"]][asset.criticity] + 1
        })
        assets_risk_scores.update({asset.id: asset.get_risk_score()})

    top_critical_assets_scores = sorted(assets_risk_scores.items(), key=operator.itemgetter(1))[::-1][:6]
    top_critical_assets = []
    for asset_id in top_critical_assets_scores:
        top_critical_assets.append(Asset.objects.get(id=asset_id[0]))

    # Format to list
    asset_grades_map_list = []
    for key in sorted(asset_grades_map.iterkeys()):
        asset_grades_map_list.append({key: asset_grades_map[key]})

    # Asset groups
    assetgroups_risk_scores = {}
    for assetgroup in AssetGroup.objects.all():
        assetgroup_grades_map[assetgroup.risk_level["grade"]].update({
            assetgroup.criticity: assetgroup_grades_map[assetgroup.risk_level["grade"]][assetgroup.criticity] + 1
        })
        assetgroups_risk_scores.update({assetgroup.id: assetgroup.get_risk_score()})

    top_critical_assetgroups_scores = sorted(assetgroups_risk_scores.items(), key=operator.itemgetter(1))[::-1][:6]
    top_critical_assetgroups = []
    for assetgroup_id in top_critical_assetgroups_scores:
        top_critical_assetgroups.append(AssetGroup.objects.get(id=assetgroup_id[0]))

    assetgroup_grades_map_list = []
    for key in sorted(assetgroup_grades_map.iterkeys()):
        assetgroup_grades_map_list.append({key: assetgroup_grades_map[key]})

    # Critical findings - Modificado
    top_critical_findings = []
    MAX_CF = 6
    for finding in findings.filter(severity="critical"):
        if len(top_critical_findings) <= MAX_CF: top_critical_findings.append(finding)
    if len(top_critical_findings) <= MAX_CF:
        for finding in findings.filter(severity="high"):
            if len(top_critical_findings) <= MAX_CF: top_critical_findings.append(finding)
    if len(top_critical_findings) <= MAX_CF:
        for finding in findings.filter(severity="medium"):
            if len(top_critical_findings) <= MAX_CF: top_critical_findings.append(finding)
    if len(top_critical_findings) <= MAX_CF:
        for finding in findings.filter(severity="low"):
            if len(top_critical_findings) <= MAX_CF: top_critical_findings.append(finding)
    if len(top_critical_findings) <= MAX_CF:
        for finding in findings.filter(severity="info"):
            if len(top_critical_findings) <= MAX_CF: top_critical_findings.append(finding)

    # CVSS - modificado
    cvss_scores = {'lte5': 0, '5to7': 0, 'gte7': 0, 'gte9': 0, 'eq10': 0}
    for finding in findings:
        if finding.risk_info["cvss_base_score"] < 5.0: cvss_scores.update({'lte5': cvss_scores['lte5']+1})
        if finding.risk_info["cvss_base_score"] >= 5.0 and finding.risk_info["cvss_base_score"] <= 7.0: cvss_scores.update({'5to7': cvss_scores['5to7']+1})
        if finding.risk_info["cvss_base_score"] >= 7.0: cvss_scores.update({'gte7': cvss_scores['gte7']+1})
        if finding.risk_info["cvss_base_score"] >= 9.0 and finding.risk_info["cvss_base_score"] < 10: cvss_scores.update({'gte9': cvss_scores['gte9']+1})
        if finding.risk_info["cvss_base_score"] == 10.0: cvss_scores.update({'eq10': cvss_scores['eq10']+1})

  # CVE & CWE
    cxe_stats = {}
    cve_list = {}
    cwe_list = {}

    finding_cves_list = Finding.objects.exclude(
            Q(vuln_refs__CVE__isnull=True)|
            Q(status__in=['mitigated', 'patched', 'closed', 'false-positive'])
        ).annotate(
            cvelist=KeyTextTransform("CVE", 'vuln_refs')
        ).values('cvelist')
    finding_cwes_list = Finding.objects.exclude(
            Q(vuln_refs__CWE__isnull=True)|
            Q(status__in=['mitigated', 'patched', 'closed', 'false-positive'])
        ).annotate(
            cwelist=KeyTextTransform("CWE", 'vuln_refs')
        ).values('cwelist')


    for finding_cves in finding_cves_list:
        for cve in ast.literal_eval(finding_cves['cvelist']):
            if cve not in cve_list.keys():
                cve_list.update({cve: 1})
            else:
                cve_list.update({cve: cve_list[cve]+1})

    for cwe_data in finding_cwes_list:
        cwe = cwe_data.values()[0]
        if cwe not in cwe_list.keys():
            cwe_list.update({cwe: 1})
        else:
            cwe_list.update({cwe: cwe_list[cwe]+1})

    cxe_stats.update({
        'top_cve': sorted(cve_list.items(), key=lambda x: x[1], reverse=True)[:10],
        'top_cwe': sorted(cwe_list.items(), key=lambda x: x[1], reverse=True)[:10],
    })



    return render(request, 'home-dashboard.html', {
        'global_stats': global_stats,
        'last_findings': last_findings,
        'last_scans': last_scans,
        'asset_grades_map': asset_grades_map_list,
        'assetgroup_grades_map': assetgroup_grades_map_list,
        'top_critical_assets': top_critical_assets,
        'top_critical_assetgroups': top_critical_assetgroups,
        'top_critical_findings': top_critical_findings,
        'cvss_scores': cvss_scores,
        'cxe_stats': cxe_stats

        })



def patch_management_view(request):
    data = []

    # date filter
    ref_date = request.GET.get('ts', None)
    if not ref_date:
        ref_date = datetime.datetime.today()
    else:
        try:
            ref_date = datetime.datetime.strptime(ref_date, '%Y/%m/%d')
        except:
            # bad date format -> today by default
            ref_date = datetime.datetime.today()

    seven_days_ago = ref_date-datetime.timedelta(days=7)
    month_ago = ref_date-datetime.timedelta(days=30)

    # asset type filter (AssetCategory)
    asset_tags = request.GET.get('asset_tags', None)
    if asset_tags:
        _asset_tags = []
        for tag in AssetCategory.objects.filter(value__iexact=asset_tags):
            print (tag)


    # Dataset 1: security fix applied 7 days max, CVSS >= 7.0
    ness_plugin_family_osupdates = [
        "aix_local_security_checks",
        "centos_local_security_checks",
        "debian_local_security_checks",
        "hp-ux_local_security_checks",
        "oracle_linux_local_security_checks",
        "red_hat_local_security_checks",
        "solaris_local_security_checks",
        "suse_local_security_checks",
        "ubuntu_local_security_checks",
        "vmware_esx_local_security_checks",
        "windows_:_microsoft_bulletins",
    ]
    dataset_7days = Asset.objects.filter(
        Q(rawfinding__created_at__gt=seven_days_ago) &
        Q(rawfinding__risk_info__vuln_publication_date__gte=seven_days_ago.strftime('%Y/%m/%d')) &
        Q(rawfinding__risk_info__cvss_base_score__gte=7.0) &
        Q(rawfinding__type__in=ness_plugin_family_osupdates)
        #Q(rawfinding__scan__engine_policy_id=1)
    #).distinct()
    ).annotate(nb_findings=Count('rawfinding')).distinct()
    print (dataset_7days)

    # Dataset 2: security fix applied 7 days max, CVSS >= 7.0, reboot required
    ness_pluginid_reboot = [
        35453, # Microsoft Windows Update Reboot Required - http://www.tenable.com/plugins/index.php?view=single&id=35453
        63756, # AIX 5.2 TL 0 : reboot - http://www.tenable.com/plugins/index.php?view=single&id=63756
        63757, # AIX 5.3 TL 0 : reboot http://www.tenable.com/plugins/index.php?view=single&id=63757
        ]
    dataset_7days_reboot = Asset.objects.filter(
        Q(rawfinding__created_at__gt=seven_days_ago) &
        Q(rawfinding__risk_info__vuln_publication_date__gte=seven_days_ago.strftime('%Y/%m/%d')) &
        Q(rawfinding__risk_info__cvss_base_score__gte=7.0) &
        Q(rawfinding__type__in=ness_plugin_family_osupdates) &
        Q(rawfinding__raw_data__plugin_information__plugin_id__in=ness_pluginid_reboot) # reboot needed
        #Q(rawfinding__scan__engine_policy_id=1)
    ).distinct()

    # Dataset 3: 30 days ago
    dataset_30days = Asset.objects.filter(
        Q(rawfinding__created_at__gt=month_ago) &
        Q(rawfinding__risk_info__vuln_publication_date__gte=month_ago.strftime('%Y/%m/%d')) &
        Q(rawfinding__risk_info__cvss_base_score__gte=7.0) &
        Q(rawfinding__type__in=ness_plugin_family_osupdates)
        #Q(rawfinding__scan__engine_policy_id=1)
    ).distinct()

    # Dataset 4: more than 30 missing patches (CVSS >= 7.0)
    dataset_30missing = Asset.objects.filter(
        #Q(rawfinding__created_at__gt=month_ago) &
        Q(rawfinding__risk_info__vuln_publication_date__gte=month_ago.strftime('%Y/%m/%d')) &
        Q(rawfinding__risk_info__cvss_base_score__gte=7.0) &
        Q(rawfinding__type__in=ness_plugin_family_osupdates)
        #Q(rawfinding__scan__engine_policy_id=1)
    ).annotate(num_missing_patches=Count('rawfinding')).filter(num_missing_patches__gte=30).distinct()

    data.append({
        "7days": dataset_7days.count(),
        "7days_reboot": dataset_7days_reboot.count(),
        "30days": dataset_30days.count(),
        "30missing": dataset_30missing.count(),
    })

    return render(request, 'patch-management-dashboard.html', { 'data': data })


def dashboard_resumido_view(request):
    findings = Finding.objects.all()
    global_stats = {
        "assets": {
            "total": Asset.objects.all().count(),
            "total_ag": AssetGroup.objects.all().count(),
        },
        "asset_types": {},
        "findings": {
            "total": findings.count(),
            "new": findings.filter(status='new').count(),
            "critical": findings.filter(severity='critical').count(),
            "high": findings.filter(severity='high').count(),
            "medium": findings.filter(severity='medium').count(),
            "low": findings.filter(severity='low').count(),
            "info": findings.filter(status='info').count(),
            "confirmed": findings.filter(status='confirmed').count(),
            "mitigated": findings.filter(status='mitigated').count(),        },
        "scans": {
            "defined": ScanDefinition.objects.all().count(),
            "performed": Scan.objects.all().count(),
            "active_periodic": ScanDefinition.objects.filter(enabled=True, scan_type='periodic').count(),
        },
        "engines": {
            "total": EngineInstance.objects.all().count(),
            "policies": EnginePolicy.objects.all().count(),
            "active": EngineInstance.objects.filter(status='READY', enabled=True).count(),
        },
        "rules": {
            "total": Rule.objects.all().count(),
            "active": Rule.objects.filter(enabled=True).count(),
            "nb_matches": 0,
        },
    }
   # update asset_types
    for at in ASSET_TYPES:
        global_stats["asset_types"].update({at[0]: Asset.objects.filter(type=at[0]).count()})

    # update nb_matches
    matches = 0
    for r in Rule.objects.all():
        matches += r.nb_matches
    global_stats["rules"].update({"nb_matches": matches})

    # Last 6 findings
    last_findings = Finding.objects.all().order_by('-id')[:6][::-1]


   # Last 6 scans
    last_scans = Scan.objects.all().order_by('-started_at')[:6]
  # Asset grades repartition and TOP 10
    asset_grades_map = {
        "A": {"high": 0, "medium": 0, "low": 0},
        "B": {"high": 0, "medium": 0, "low": 0},
        "C": {"high": 0, "medium": 0, "low": 0},
        "D": {"high": 0, "medium": 0, "low": 0},
        "E": {"high": 0, "medium": 0, "low": 0},
        "F": {"high": 0, "medium": 0, "low": 0},
        "-": {"high": 0, "medium": 0, "low": 0}
    }

    assetgroup_grades_map = copy.deepcopy(asset_grades_map)



    # Asset grades
    assets_risk_scores = {}
    for asset in Asset.objects.all():
        asset_grades_map[asset.risk_level["grade"]].update({
            asset.criticity: asset_grades_map[asset.risk_level["grade"]][asset.criticity] + 1
        })
        assets_risk_scores.update({asset.id: asset.get_risk_score()})



    top_critical_assets_scores = sorted(assets_risk_scores.items(), key=operator.itemgetter(1))[::-1][:6]
    top_critical_assets = []
    for asset_id in top_critical_assets_scores:
        top_critical_assets.append(Asset.objects.get(id=asset_id[0]))
    # Format to list
    asset_grades_map_list = []
    for key in sorted(asset_grades_map.iterkeys()):
        asset_grades_map_list.append({key: asset_grades_map[key]})

 # Asset groups
    assetgroups_risk_scores = {}
    for assetgroup in AssetGroup.objects.all():
        assetgroup_grades_map[assetgroup.risk_level["grade"]].update({
            assetgroup.criticity: assetgroup_grades_map[assetgroup.risk_level["grade"]][assetgroup.criticity] + 1
        })
        assetgroups_risk_scores.update({assetgroup.id: assetgroup.get_risk_score()})

    top_critical_assetgroups_scores = sorted(assetgroups_risk_scores.items(), key=operator.itemgetter(1))[::-1][:6]
    top_critical_assetgroups = []
    for assetgroup_id in top_critical_assetgroups_scores:
        top_critical_assetgroups.append(AssetGroup.objects.get(id=assetgroup_id[0]))

    assetgroup_grades_map_list = []
    for key in sorted(assetgroup_grades_map.iterkeys()):
        assetgroup_grades_map_list.append({key: assetgroup_grades_map[key]})


    # Critical findings - Modificado
    top_critical_findings = []
    MAX_CF = 6
    for finding in findings.filter(severity="critical"):
        if len(top_critical_findings) <= MAX_CF: top_critical_findings.append(finding)
    if len(top_critical_findings) <= MAX_CF:
        for finding in findings.filter(severity="high"):
            if len(top_critical_findings) <= MAX_CF: top_critical_findings.append(finding)
    if len(top_critical_findings) <= MAX_CF:
        for finding in findings.filter(severity="medium"):
            if len(top_critical_findings) <= MAX_CF: top_critical_findings.append(finding)
    if len(top_critical_findings) <= MAX_CF:
        for finding in findings.filter(severity="low"):
            if len(top_critical_findings) <= MAX_CF: top_critical_findings.append(finding)
    if len(top_critical_findings) <= MAX_CF:
        for finding in findings.filter(severity="info"):
            if len(top_critical_findings) <= MAX_CF: top_critical_findings.append(finding)

    # CVSS - modificado
    cvss_scores = {'lte5': 0, '5to7': 0, 'gte7': 0, 'gte9': 0, 'eq10': 0}
    for finding in findings:
        if finding.risk_info["cvss_base_score"] < 5.0: cvss_scores.update({'lte5': cvss_scores['lte5']+1})
        if finding.risk_info["cvss_base_score"] >= 5.0 and finding.risk_info["cvss_base_score"] <= 7.0: cvss_scores.update({'5to7': cvss_scores['5to7']+1})
        if finding.risk_info["cvss_base_score"] >= 7.0: cvss_scores.update({'gte7': cvss_scores['gte7']+1})
        if finding.risk_info["cvss_base_score"] >= 9.0 and finding.risk_info["cvss_base_score"] < 10: cvss_scores.update({'gte9': cvss_scores['gte9']+1})
        if finding.risk_info["cvss_base_score"] == 10.0: cvss_scores.update({'eq10': cvss_scores['eq10']+1})

  # CVE & CWE
    cxe_stats = {}
    cve_list = {}
    cwe_list = {}

    finding_cves_list = Finding.objects.exclude(
            Q(vuln_refs__CVE__isnull=True)|
            Q(status__in=['mitigated', 'patched', 'closed', 'false-positive'])
        ).annotate(
            cvelist=KeyTextTransform("CVE", 'vuln_refs')
        ).values('cvelist')
    finding_cwes_list = Finding.objects.exclude(
            Q(vuln_refs__CWE__isnull=True)|
            Q(status__in=['mitigated', 'patched', 'closed', 'false-positive'])
        ).annotate(
            cwelist=KeyTextTransform("CWE", 'vuln_refs')
        ).values('cwelist')



    for finding_cves in finding_cves_list:
        for cve in ast.literal_eval(finding_cves['cvelist']):
            if cve not in cve_list.keys():
                cve_list.update({cve: 1})
            else:
                cve_list.update({cve: cve_list[cve]+1})
    for cwe_data in finding_cwes_list:
        cwe = cwe_data.values()[0]
        if cwe not in cwe_list.keys():
            cwe_list.update({cwe: 1})
        else:
            cwe_list.update({cwe: cwe_list[cwe]+1})

    cxe_stats.update({
        'top_cve': sorted(cve_list.items(), key=lambda x: x[1], reverse=True)[:10],
        'top_cwe': sorted(cwe_list.items(), key=lambda x: x[1], reverse=True)[:10],
    })

    return render(request, 'dashboard-resumido.html', {
        'global_stats': global_stats,
        'last_findings': last_findings,
        'last_scans': last_scans,
        'asset_grades_map': asset_grades_map_list,
        'assetgroup_grades_map': assetgroup_grades_map_list,
        'top_critical_assets': top_critical_assets,
        'top_critical_assetgroups': top_critical_assetgroups,
        'top_critical_findings': top_critical_findings,
        'cvss_scores': cvss_scores,
        'cxe_stats': cxe_stats,

        })



# Adicionado para Relatorio de Billing"
def billing_statement_view(request):
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
    return render(request, 'report-asset-statement.html', {
        'assets': assets,
        'asset_groups': asset_groups,

})
