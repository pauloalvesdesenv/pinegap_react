# -*- coding: utf-8 -*-
from django.conf.urls import url
from .import views, apis
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin


urlpatterns = [
    ## WEB Views
    # ex: /settings/
    url(r'^$', views.show_settings_menu, name='show_settings_menu'),
    # Whitelabel  Views
    url(r'^add$', views.add_brand_view, name='add_brand_view'),
    url(r'^$', views.user_details_view, name='user_details_view'),
    url(r'^edit/(?P<whitelabel_id>[0-9]+)$', views.edit_brand_view, name='edit_brand_view'),
    url(r'^$', views.show_whitelabel_view, name='show_whitelabel_view'),
    


    ## API views
    # ex: /settings/api/v1/update
    url(r'^api/v1/update$', apis.update_setting_api, name='update_setting_api'),
    # ex: /settings/api/v1/add
    url(r'^api/v1/add$', apis.add_setting_api, name='add_setting_api'),
    # ex: /settings/api/v1/delete/3
    url(r'^api/v1/delete/(?P<setting_id>[0-9]+)$', apis.delete_setting_api, name='delete_setting_api'),
    # ex: /settings/api/v1/export
    url(r'^api/v1/export$', apis.export_settings_api, name='export_settings_api'),
    # ex: /whitelabels/api/v1/get
    url(r'^api/v1/get$', apis.get_api, name='get_api'),

]
