from django.contrib.auth import views as auth_views

urlpatterns = [
    ...
	# Views URLs  PASSWORD RESET
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),

	# View URLs WHITELABEL
    url(r'^$', views.show_whitelabel_base, name='show_whitelabel_base'),
    url(r'^$', views.show_whitelabel_home, name='show_whitelabel_home'),
    url(r'^$', views.show_whitelabel_login, name='show_whitelabel_login'),
    url(r'^edit/(?P<id>\d+)/$', views.edit_whitelabel_view, name='edit_whitelabel_view'),
    url(r'^add$', views.add_whitelabel_view, name='add_whitelabel_view'),
    url(r'^edit/(?P<id>\d+)/$', views.edit_whitelabel_view, name='edit_whitelabel_view'),
    url(r'^$', views.show_whitelabel_brand, name='show_whitelabel_brand'),

	# Apis URLs WHITELABEL
    url(r'^api/v1/whitelabels', apis.whitelabels_api, name='whitelabels_api'),

]


