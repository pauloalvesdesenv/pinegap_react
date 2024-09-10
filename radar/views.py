# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render #
from django.db.models import Q, Count #
from rules.models import Rule
from datetime import timedelta
from pytz import timezone
import shlex #
import json #
import datetime
import operator
import copy
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Count
from assets.models import Asset, AssetGroup, ASSET_TYPES
from findings.models import Finding
from scans.models import Scan, ScanDefinition
from engines.models import EngineInstance, EnginePolicy
from rules.models import Rule
from django.db.models import Count, F


#####################  RADAR - BY BILL  ###################
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone as tz
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, F
from django_celery_beat.models import PeriodicTask, IntervalSchedule

from app.settings import TIME_ZONE
from scans.forms import ScanDefinitionForm
from scans.models import Scan, ScanDefinition
from scans.utils import _update_celerybeat, _run_scan
from engines.models import Engine, EnginePolicy, EngineInstance, EnginePolicyScope
from findings.models import RawFinding
from assets.models import Asset, AssetGroup

from datetime import timedelta, datetime
from pytz import timezone
import shlex
import json
###########################################################



def radar_view(request):
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
            "info": findings.filter(severity='info').count(),
        },
        "scans": {
            "defined": ScanDefinition.objects.all().count(),
            "performed": Scan.objects.all().count(),
            "active_periodic": ScanDefinition.objects.filter(enabled=True, scan_type='periodic').count(),
            #"a_periodic": ScanDefinition.objects.filter(enabled=True, scan_type='periodic'),
            #"minutes": ScanDefinition.objects.filter(period='minutes'),
            #"hours": ScanDefinition.objects.filter(period='hours'),
            #"seconds": ScanDefinition.objects.filter(period='seconds'),
            #"days": ScanDefinition.objects.filter(period='days'),
            #"recorrency": ScanDefinition.objects.filter(every='0'),
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

    # Recorrencia
    recorrencia = ScanDefinition.objects.all().order_by('-id')[:90][::-1]

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

    # Critical findings
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
    cvss_scores = {'lte5': 0, '5to7': 0, 'gte7': 0, 'gte9': 0, 'eq10': 0}
    for finding in findings:
        if finding.risk_info["cvss_base_score"] < 5.0: cvss_scores.update({'lte5': cvss_scores['lte5']+1})
        if finding.risk_info["cvss_base_score"] >= 5.0 and finding.risk_info["cvss_base_score"] <= 7.0: cvss_scores.update({'5to7': cvss_scores['5to7']+1})
        if finding.risk_info["cvss_base_score"] >= 7.0: cvss_scores.update({'gte7': cvss_scores['gte7']+1})
        if finding.risk_info["cvss_base_score"] >= 9.0 and finding.risk_info["cvss_base_score"] < 10: cvss_scores.update({'gte9': cvss_scores['gte9']+1})
        if finding.risk_info["cvss_base_score"] == 10.0: cvss_scores.update({'eq10': cvss_scores['eq10']+1})
    return render(request, 'radar.html', {
        'global_stats': global_stats,
        'last_findings': last_findings,
        'recorrencia':recorrencia,
        'last_scans': last_scans,
        'asset_grades_map': asset_grades_map_list,
        'assetgroup_grades_map': assetgroup_grades_map_list,
        'top_critical_assets': top_critical_assets,
        'top_critical_assetgroups': top_critical_assetgroups,
        'top_critical_findings': top_critical_findings,
        'cvss_scores': cvss_scores
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
    return render(request, 'radar.html', { 'data': data })


# Scan Definitions
def list_scan_def_view(request):
    scans = Scan.objects.all()
    scan_defs = ScanDefinition.objects.all().order_by('-updated_at').annotate(scan_count=Count('scan')).annotate(engine_type_name=F('engine_type__name'))
    return render(request, 'radar.html', {
        'scan_defs': scan_defs, 'scans': scans})

def detail_scan_def_view(request, scan_definition_id):
    """Details of a scan definition."""
    scan_def = get_object_or_404(ScanDefinition, id=scan_definition_id)
    scan_list = scan_def.scan_set.order_by('-finished_at')
    paginator = Paginator(scan_list, 20)
    page = request.GET.get('page')
    try:
        scans = paginator.page(page)
    except PageNotAnInteger:
        scans = paginator.page(1)
    except EmptyPage:
        scans = paginator.page(paginator.num_pages)
    return render(request, 'radar.html', {
        'scan_def': scan_def, 'scans': scans})


def list_scans_view(request):
    """List performed scans."""
    scan_list = Scan.objects.all().order_by('-finished_at')

    paginator = Paginator(scan_list, 10)
    page = request.GET.get('page')
    try:
        scans = paginator.page(page)
    except PageNotAnInteger:
        scans = paginator.page(1)
    except EmptyPage:
        scans = paginator.page(paginator.num_pages)
    return render(request, 'radar.html', {'scans': scans})



################### RADAR DETAIL - BY BILL #######################

def detail_scan_view(request, scan_id):
    # todo: optimize that shit
    scan = get_object_or_404(Scan, id=scan_id)
    scan.update_sumary()
    scan.save()
    scan_def = ScanDefinition.objects.get(id=scan.scan_definition.id)

    # Check search filters
    search_filters = request.GET.get("search", None)
    parsed_filters = ""
    assets_filters = {}
    findings_filters = {}

    if search_filters:
        parsed_filters = shlex.shlex(search_filters)
        parsed_filters.whitespace_split = True
        parsed_filters.quotes = '"'
        parsed_filters.wordchars += '\''

        for fil in parsed_filters:
            if fil.startswith("\""):
                fil = fil.lstrip('"')
                fil = fil.rstrip('"')
            if fil.startswith("assets:") or fil.startswith("a:") or fil.startswith("assets.value:") or fil.startswith("a.value:"):
                assets_filters.update({"value__icontains": fil.split(':')[1]})
            elif fil.startswith("asset.criticity:") or fil.startswith("a.criticity:"):
                assets_filters.update({"criticity__icontains": fil.split(':')[1]})
            elif fil.startswith("asset.type:") or fil.startswith("a.type:"):
                assets_filters.update({"type__icontains": fil.split(':')[1]})
            elif fil.startswith("finding:") or fil.startswith("f:") or fil.startswith("finding.title:") or fil.startswith("f.title:"):
                findings_filters.update({"title__icontains": fil.split(':')[1]})
            elif fil.startswith("finding.status:") or fil.startswith("f.status:"):
                findings_filters.update({"status__icontains": fil.split(':')[1]})
            elif fil.startswith("finding.severity:") or fil.startswith("f.severity:"):
                findings_filters.update({"severity__icontains": fil.split(':')[1]})
            else:
                assets_filters.update({"value__icontains": fil})
                findings_filters.update({"title__icontains": fil})

    # Search assets related to the scan
    if assets_filters == {}:
        assets = scan.assets.all()
    else:
        assets = scan.assets.filter(**assets_filters)
        findings_filters.update({"asset__in": assets})

    # Search asset groups related to the scan
    assetgroups = scan_def.assetgroups_list.all()

    # Add the assets from the asset group to the existing list of assets
    if len(assetgroups) == 0:
        other_assets = assets
    else:
        other_assets = []
        for asset in assets:
            for ag in assetgroups:
                if asset not in ag.assets.all():
                    other_assets.append(asset)

    # Search raw findings related to the asset
    if findings_filters == {}:
        raw_findings = RawFinding.objects.filter(scan=scan).order_by('asset', 'severity', 'type', 'title')
    else:
        findings_filters.update({"scan": scan})
        raw_findings = RawFinding.objects.filter(**findings_filters).order_by('asset', 'severity', 'type', 'title')



    # Generate summary info on assets (for progress bars)
    summary_assets = {}
    for a in assets:
        summary_assets.update({a.value: {"info": 0, "low": 0, "medium": 0, "high": 0, "critical": 0, "total": 0}})
    for f in raw_findings.filter(asset__in=assets):
        summary_assets[f.asset_name].update({
            f.severity: summary_assets[f.asset_name][f.severity] + 1,
            "total": summary_assets[f.asset_name]["total"] + 1
           })

    # Generate summary info on asset groups (for progress bars)
    summary_assetgroups = {}
    for ag in assetgroups:
        summary_assetgroups.update({
            ag.id: {
                "info": 0, "low": 0, "medium": 0,
                "high": 0, "critical": 0, "total": 0
            }
        })
        for f in raw_findings:
            if f.asset.value in ag.assets.all().values_list('value', flat=True):
                summary_assetgroups[ag.id].update({
                    f.severity: summary_assetgroups[ag.id][f.severity] + 1,
                    "total": summary_assetgroups[ag.id]["total"] + 1
                })

        for f in raw_findings:
            if f.asset.value in ag.assets.all().values_list('value', flat=True):
                summary_assetgroups[ag.id].update({
                    f.severity: summary_assetgroups[ag.id][f.severity] + 1,
                    "total": summary_assetgroups[ag.id]["total"] + 1
                })

    # Generate findings stats
    month_ago = datetime.today()-timedelta(days=30)
    findings_stats = {
        "count": raw_findings.count(),
        "cvss_gte_70": raw_findings.filter(risk_info__cvss_base_score__gte=7.0).count(),
        "pubdate_30d": raw_findings.filter(risk_info__vuln_publication_date__lte=month_ago.strftime('%Y/%m/%d')).count(),
        "cvss_gte_70_pubdate_30d": raw_findings.filter(risk_info__cvss_base_score__gte=7.0, risk_info__vuln_publication_date__lte=month_ago.strftime('%Y/%m/%d')).count()
    }

 # Pagination of assets
#    paginator_assets = Paginator(assets, 20)
#    page_assets = request.GET.get('p_assets', None)
#    try:
#        scan_assets = paginator_assets.page(page_assets)
#    except PageNotAnInteger:
#        scan_assets = paginator_assets.page(1)
#    except EmptyPage:
#        scan_assets = paginator_assets.page(paginator_assets.num_pages)

   # Pagination of findings
    scan_findings = raw_findings
    paginator_findings = Paginator(raw_findings, 50)
    page_finding = request.GET.get('p_findings')
    try:
        scan_findings = paginator_findings.page(page_finding)
    except PageNotAnInteger:
        scan_findings = paginator_findings.page(1)
    except EmptyPage:
        scan_findings = paginator_findings.page(paginator_findings.num_pages)

    # Pagination of events
    scan_events = scan.event_set.all().order_by('-id')
    paginator_events = Paginator(scan_events, 50)
    page_event = request.GET.get('p_events')
    try:
        scan_events = paginator_events.page(page_event)
    except PageNotAnInteger:
        scan_events = paginator_events.page(1)
    except EmptyPage:
        scan_events = paginator_events.page(paginator_events.num_pages)

    return render(request, 'radar.html', {
        'scan': scan,
        'summary_assets': summary_assets,
        'summary_assetgroups': summary_assetgroups,
        'assets': assets,
        'assetgroups': assetgroups,
        'other_assets': other_assets,
        'findings': scan_findings,
        'findings_stats': findings_stats,
        'scan_events': scan_events})
