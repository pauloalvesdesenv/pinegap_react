#-*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_d
from django.contrib.auth import update_session_auth_hash #Password Reset
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm  #Password Reset
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model  #
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from users.serializers import UserSerializer
from users.forms import LoginForm
from reportings.views import homepage_dashboard_view
from users.forms import UserCreationForm
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext, ugettext_lazy as _
from django.core.exceptions import PermissionDenied
from users.models import Join

####### USER TREE UPDATE VIEW - BY Bill #########
from django.views.generic import UpdateView


##############Implement Control Access of Url - By BILL##############
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404

######################################################################




class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@login_required(login_url="login/")
def home(request):
    # get logged user info:
    #
    # ## Assets
    # # OK- total number of assets
    # # OK- number of asset groups
    # # OK- number of assets by criticity
    # # - number of findings by asset
    # assets_stats = {}
    # assets = Asset.objects.filter(owner_id=request.user.id)
    # assets_stats.update({'count': assets.count()})
    # assets_stats.update({'count_low': assets.filter(criticity='low').count()})
    # assets_stats.update({'count_medium': assets.filter(criticity='medium').count()})
    # assets_stats.update({'count_high': assets.filter(criticity='high').count()})
    #
    # asset_groups = AssetGroup.objects.filter(owner_id=request.user.id)
    # assets_stats.update({'countgroups': asset_groups.count()})
    # assets_stats.update({'countgroups_low': asset_groups.filter(criticity='low').count()})
    # assets_stats.update({'countgroups_medium': asset_groups.filter(criticity='medium').count()})
    # assets_stats.update({'countgroups_high': asset_groups.filter(criticity='high').count()})
    #
    # ## Findings
    # # OK- total number of findings
    # # OK- number of findings by criticity
    # findings_stats = {}
    # findings = Finding.objects.filter(owner_id=request.user.id)
    # findings_stats.update({'count': findings.count()})
    # findings_stats.update({'count_info': findings.filter(severity='info').count()})
    # findings_stats.update({'count_low': findings.filter(severity='low').count()})
    # findings_stats.update({'count_medium': findings.filter(severity='medium').count()})
    # findings_stats.update({'count_high': findings.filter(severity='high').count()})
    #
    #
    # ## Scans
    # # OK- total number of scans performed
    # # OK- total number of active periodic scans
    # scans_stats = {}
    # scans = Scan.objects.filter(owner_id=request.user.id)
    # scan_definitions = ScanDefinition.objects.filter(owner_id=request.user.id)
    # scan_campaigns = ScanCampaign.objects.filter(owner_id=request.user.id)
    # scans_stats.update({'count_scans': scans.count()})
    # scans_stats.update({'count_scan_definitions': scan_definitions.count()})
    # scans_stats.update({'count_scan_campaigns': scan_campaigns.count()})
    # scans_stats.update({'count_active_periodic_scans': scan_definitions.filter(enabled=True).count()})
    #
    #
    # ## Engines
    # # OK- total number of engines configured
    # # OK- total number of engine instances configured
    # # - number of active engine instances
    # # - number of policies by engine
    # engines_stats = {}
    # engines = Engine.objects.all()
    # engines_stats.update({"count": engines.count()})
    # engines_stats.update({"names": ", ".join([e.name for e in engines])})

    # return render(request,"home.html", {
    #     'assets': assets_stats,
    #     'findings': findings_stats,
    #     'scans': scans_stats,
    #     'engines': engines_stats,
    #      })
    return redirect(homepage_dashboard_view)

@csrf_exempt
def login(request):
    default_form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        user = authenticate(request, username=form.data["username"], password=form.data["password"])
        if user is not None:
            if user.is_active:
                login_d(request, user)
                return redirect('homepage_dashboard_view')
            else:
                return render(request, 'login.html', {'form': form})
        else:
            return render(request, 'login.html', {'form': form})
    else:
        return render(request, 'login.html', {'form': default_form})

@csrf_exempt
def logout(request):
       logout(request)
       response = HttpResponseRedirect('/login')
       response.delete_cookie('sessionid')
       response.delete_cookie('cookie_sessionid')
       return render(request, 'login.html', {'form': default_form})


#@csrf_exempt
#def signup(request):
#    if request.method == 'POST':
#        form = UserCreationForm(request.POST)
#        if form.is_valid():
#            form.save()
#            username = form.cleaned_data.get('username')
 #          first_name = form.cleaned_data.get('first_name')
 #          last_name = form.cleaned_data.get('last_name')
 #          email = form.cleaned_data.get('email')
#            raw_password = form.cleaned_data.get('password1')
#            user = authenticate(username=username, password=raw_password)
#            login_d(request, user)
#            return redirect('homepage_dashboard_view')
#    else:
#        form = UserCreationForm()
#    return render(request, 'signup.html', {'form': form})



# Add Bloqueio de URL - By BILL
@user_passes_test(lambda u: u.groups.filter(name='visitante').count() == 0, login_url='/users/deny/')
@user_passes_test(lambda u: u.groups.filter(name='analista').count() == 0,  login_url='/users/deny/')
@user_passes_test(lambda u: u.groups.filter(name='dpo').count() == 0, login_url='/users/deny/')
def user_details_view(request):
    user = get_object_or_404(User, id=request.user.id)
    groups = Group.objects.all()
    apitokens = Token.objects.filter(user=request.user)
    if apitokens.count() >= 1:
        apitoken = apitokens[0]
    else:
        apitoken = ""
    return render(request, 'details-user.html', {
        'user': user,
        'groups': groups,
        'apitoken': apitoken
    })

# Add Bloqueio de URL - By BILL
@user_passes_test(lambda u: u.groups.filter(name='visitante').count() == 0, login_url='/users/deny/')
@user_passes_test(lambda u: u.groups.filter(name='analista').count() == 0,  login_url='/users/deny/')
@user_passes_test(lambda u: u.groups.filter(name='dpo').count() == 0, login_url='/users/deny/')
#superuser
def list_users_view(request):
#    users = User.objects.all()
    users = User.objects.exclude(is_superuser=True)

   # return render(request, 'list-users.html', {'users': users})
    if request.user.is_superuser:
        return User.objects.all()
        return User.objects.filter(is_superuser=True)
        return User.objects.filter(is_active=True)
        return User.objects.exclude(is_active=False)
    return render(request, 'list-users.html', {'users': users}) #add para teste



# Add Bloqueio de URL - By BILL
@user_passes_test(lambda u: u.groups.filter(name='visitante').count() == 0, login_url='/users/deny/')
@user_passes_test(lambda u: u.groups.filter(name='analista').count() == 0,  login_url='/users/deny/')
@user_passes_test(lambda u: u.groups.filter(name='dpo').count() == 0, login_url='/users/deny/')
@csrf_exempt
def add_user_view(request):
    queryset = Group.objects.filter(name=['visitante', 'gestor', 'analista', 'dpo'])
    if request.method == 'GET':
        form = UserCreationForm()
    elif request.method == 'POST':

        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email'],
            )
            group = form.cleaned_data['group']
            user.groups.add(group)

            messages.success(request, 'Usuário criado com sucesso')
            return redirect('/settings/#users')

    return render(request, 'add-user.html', {'form': form})



def edit_user_password_view(request):
    form = None
    if request.method == 'GET':
        form = PasswordChangeForm(user=request.user)
    elif request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Sua senha foi modificada com sucesso!')
        else:
            messages.error(request, 'Por favor corrija os erros abaixo:')
        if request.user.is_superuser:
            return redirect('show_settings_menu')

    return render(request, 'change-password.html', {'form': form})

def unactive_user(request, user_id):
    user = User.objects.get(pk=user_id)
    user.is_active = False
    user.profile.status = "DISABLED"
    user.save()
    return redirect('/settings/#users')

def active_user(request, user_id):
    user = User.objects.get(pk=user_id)
    user.is_active = True
    user.profile.status = "ACTIVE"
    user.save()
    return redirect('/settings/#users')

def change_user_group(request, user_id):
    user = User.objects.get(pk=user_id)
    group = Group.objects.get(pk=request.POST.get('id_group'))
    user_groups = user.groups.all()
    if user_groups:
        for user_group in user_groups:
            user_group.user_set.remove(user)
    group.user_set.add(user)
    return redirect('/settings/#users')






class CustomBackend(ModelBackend):  # requires to define two functions authenticate and get_user

    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()

        try:
            # below line gives query set,you can change the queryset as per your requirement
            user = UserModel.objects.filter(
                Q(username__iexact=username) |
                Q(email__iexact=username)
            ).distinct()

        except UserModel.DoesNotExist:
            return None

        if user.exists():
            ''' get the user object from the underlying query set,
            there will only be one object since username and email
            should be unique fields in your models.'''
            user_obj = user.first()
            if user_obj.check_password(password):
                return user_obj
            return None
        else:
            return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None


################ USER  PROFILE UPDATE RECORDS - BY Bill  #########

class UserProfileUpdateView(UpdateView):
    model = User

    def get_initial(self):
        initial = super(UserProfileUpdateView, self).get_initial()
        try:
            current_group = self.object.groups.get()
        except:
            # exception can occur if the edited user has no groups
            # or has more than one group
            pass
        else:
            initial['group'] = current_group.pk
        return initial

    def get_form_class(self):
        return UserCreationForm

    def form_valid(self, form):
        self.object.groups.clear()
        self.object.groups.add(form.cleaned_data['group'])
        return super(UserProfileUpdateView, self).form_valid(form)
