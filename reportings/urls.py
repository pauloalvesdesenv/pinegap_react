from __future__ import unicode_literals
from django.views.generic import TemplateView

from django.conf.urls import url
from django.contrib import admin
from . import views
from . import api


urlpatterns = [
    # VIEWS
    # ex: /reportings/patch_management
    url(r'^patch_management$', views.patch_management_view, name='patch_management_view'),
    # ex: /reportings/dashboard
    url(r'^dashboard$', views.homepage_dashboard_view, name='homepage_dashboard_view'),
    # ex: /reportings/dashboard
    url(r'^dashboard-resumido$', views.dashboard_resumido_view, name='dashboard_resumido_view'),
    # ex: /reportings/billing
    url(r'^billing$', views.billing_statement_view, name='billing_statement_view'),



    ## API -dashboard api viewport
    url(r'^api/v1/global_stats$', api.global_stats_api, name='global_stats_api'),
    ## API1 - dashboard resumido report viewport
    url(r'^api/v1/dashboard-resumido$', api.dashboard_resumido_api, name='dashboard_resumido_api'),
    ## API2 - Assets Deleteds
    url(r'^api/v1/assets-deleted$', api.deleted_assets_api, name='deleted_assets_api'),
    ## API3 - Assets Atuais
    url(r'^api/v1/assets-using$', api.using_assets_api, name='using_assets_api'),
    ## API4 - Assets History
    url(r'^api/v1/assets-history$', api.history_assets_api, name='history_assets_api'),
    ## API5 - Billing Report
    url(r'^api/v1/billing$', api.billing_statement_api, name='billing_statement_api'),
    ## API6 - Matriz Quantitativa
    url(r'^api/v1/matriz$', api.matriz_risco_quantitativo_api, name='matriz_risco_quantitativo_api'),





    #url(r'^"https://nvd.nist.gov/vuln/detail/{{cve.0}}"/', TemplateView.as_view(template_name="https://nvd.nist.gov/vuln/detail/{{cve.0}}"),
    #               name='cve'),
]
