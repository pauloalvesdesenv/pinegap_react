from django.conf.urls import url
from django.contrib import admin
from . import views, api
#from . import api
from scans import apis

urlpatterns = [
    # VIEWS
    # ex: /reportings/patch_management
    url(r'^radar$', views.radar_view, name='radar_view'),
    #url(r'^dashboard$', views.homepage_dashboard_view, name='homepage_dashboard_view'),
    # ex: /scans/defs/list
    url(r'^defs/list$', views.list_scan_def_view, name='list_scan_def_view'),
    # ex: /scans/defs/details/33
    url(r'^defs/details/(?P<scan_definition_id>[0-9]+)$', views.detail_scan_def_view, name='detail_scan_def_view'),
    # ex: /scans/defs/list
    url(r'^list$', views.list_scans_view, name='list_scans_view'),
    # ex: /scans/details/33
    url(r'^details/(?P<scan_id>[0-9]+)$', views.detail_scan_view, name='detail_scan_view'),
    # ex: /scans/defs/details/33
    url(r'^defs/details/(?P<scan_definition_id>[0-9]+)$', views.detail_scan_def_view, name='detail_scan_def_view'),


    ## API
    url(r'^api/v1/global_stats$', api.global_stats_api, name='global_stats_api'),
    # ex: /scans/api/v1/defs/list
    url(r'^api/v1/defs/list$', apis.get_scan_definitions_api, name='get_scan_definitions_api'),
    # ex: /scans/api/v1/stats
    url(r'^api/v1/stats$', apis.get_scans_stats_api, name='get_scans_stats_api'),
    # ex: /scans/api/v1/defs/by-id/1
    url(r'^api/v1/defs/by-id/(?P<scan_id>[0-9]+)$', apis.get_scan_definition_api, name='get_scan_definition_api'),
]
