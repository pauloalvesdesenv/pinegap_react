# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from django.views.generic import TemplateView
from rest_framework_swagger.views import get_swagger_view
from users import views as user_views
from users.views import unactive_user
# add url path
#from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers






def i18n_javascript(request):
    return admin.site.i18n_javascript(request)


api_schema_view = get_swagger_view(title='PineGap Platform REST-API')

urlpatterns = [
    url(r'^apis-doc', api_schema_view),
    url(r'^admin/', admin.site.urls),
    url(r'^engines/', include('engines.urls')),
    url(r'^currencies/', include('currencies.urls')),
    url(r'^findings/', include('findings.urls')),
    url(r'^assets/', include('assets.urls')),
    url(r'^users/', include('users.urls')),
    url(r'^radar/', include('radar.urls')),
    url(r'^scans/', include('scans.urls')),
    url(r'^events/', include('events.urls')),
    url(r'^rules/', include('rules.urls')),
    url(r'^reportings/', include('reportings.urls')),
    url(r'^settings/', include('settings.urls')),
    url(r'^whitelabels/', include('whitelabels.urls')),
    url(r'^search', include('search.urls')),
    url(r'^', include('users.urls'), name='home'),
    url(r'^login$', user_views.login, name='login'),
    url(r'^logout$', auth_views.logout, {'next_page': '/login'}, name='logout'),
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    #url(r'^admin/jsi18n/', i18n_javascript),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico')),
    
    
#   url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.MEDIA_ROOT}),
]

# debug toolbar & download file
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

urlpatterns += staticfiles_urlpatterns()

