#    from __future__ import unicode_literals
#    from django.conf.urls.static import static
#    from django.conf import settings
#    from django.contrib import admin
#    from django.contrib.auth import views as auth_views
#    from django.urls import include, path

#    from . import views
#urlpatterns = [
#    ...
#    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
#    path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
#    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
#    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
#    path('accounts/', include('django.contrib.auth.urls')),
#]

from django.urls import include, path
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from __future__ import unicode_literals
from django.urls import path
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView

from . import views

app_name = 'password_reset'
urlpatterns = [
#  path('signup/', views.SignUpView.as_view(), name='signup'),
#  path('login/', views.LoginView.as_view(), name='login'),
#  path('logout/', views.LogOutView.as_view(), name='logout'),
    path('password-change/', views.PasswordChangeView.as_view(),
         name='password-change'),
    path('password_reset/', views.PasswordResetView.as_view(), #replace - by _
         name='password_reset'), #replace - by _
    path('password_reset_done/', views.PasswordResetDoneView.as_view(),
         name='password_reset_done'), #replace - by _
   path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
         views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
]
