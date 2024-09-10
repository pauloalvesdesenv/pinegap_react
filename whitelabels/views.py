# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# match
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.postgres.aggregates import ArrayAgg
import csv
import copy
####


from django.conf.urls import url
#from . import views, apis

###########################

from django.template import RequestContext #image

from django.db.models import Value, CharField, Case, When, Q, Count
from django.shortcuts import render, redirect  #WL upl Fls

from .forms import WhitelabelForm
from django.contrib.auth.models import User
from django.db.models import F
from rest_framework.authtoken.models import Token
from events.models import Event
from users.views import user_details_view
import base64
from django.contrib import messages
from django.contrib.postgres.aggregates import ArrayAgg
from django.views.generic.edit import FormView # Upload Files
from .models import Whitelabel
from .models import Brand

from settings.models import Setting
from django.conf import settings # Upload Files

from django.core.files.storage import FileSystemStorage # Upload Files
from django.conf.urls.static import static

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from users.serializers import UserSerializer


from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import get_user_model  #
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from .forms import WhitelabelForm
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
#from django.views.generic import TemplateView

from django.http import JsonResponse
##################### REST FRAMEWORK SETUP ######################
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

#Plus Api View Renderer
from rest_framework.renderers import TemplateHTMLRenderer

# Form
from common.utils import encoding

##############Implement Control Access of Url - By BILL##############
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404

######################################################################



def show_whitelabel_menu(request):
    """View: List settings menus."""
    from cursor_pagination import CursorPaginator

    users = User.objects.exclude(username="admin", is_active="False").annotate(apitoken=F('auth_token'))
    settings = Setting.objects.all().order_by("key")
    events_list = Event.objects.all()
    whitelabels  = Brand.objects.all()

    nb_rows = int(request.GET.get('n', 80))
    events_paginator = CursorPaginator(events_list, ordering=['id'])
    page_events = request.GET.get('p_events', 1)
    if type(page_events) == 'unicode' and not page_events.isnumeric():
        page_events = 1
    else:
        page_events = int(page_events)
    if page_events > 0:
        after = base64.b64encode(str((page_events-1)*nb_rows))
    else:
        after = base64.b64encode("0")

    events = events_paginator.page(first=nb_rows, after=after)
    has_previous = after is not None and base64.b64decode(after) > "0"
    previous_decoded_cursor = "1"
    if after is not None and base64.b64decode(after) > "0":
        previous_decoded_cursor = page_events - 1
    next_decoded_cursor = "1"
    if events.has_next:
        next_decoded_cursor = page_events + 1



    return render(request, 'menu-whitelabel.html', {
        'users': users,
        'settings': settings,
        'events': events,
	'whitelabels': whitelabels,
        'events_page_info': {
            'end_cursor': events_list.count()//nb_rows,
            'has_previous': has_previous,
            'has_next': events.has_next,
            'next_page_number': next_decoded_cursor,
            'previous_page_number': previous_decoded_cursor
        }
    })



def user_details_view(request):
    user = get_object_or_404(User, id=request.user.id)
    apitokens = Token.objects.filter(user=request.user)
    if apitokens.count() >= 1:
        apitoken = apitokens[0]
    else:
        apitoken = ""
    return render(request, 'menu-user.html', {
        'user': user,
        'apitoken': apitoken
    })


def show_whitelabel_brand(request):
     branding = Brand.objects.all()

     return render(request, 'menu-whitelabel.html', {
        'branding': branding
    })




class Get_Api(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'menu-whitelabel.html'

    def get(self, request):
        queryset = Brand.objects.all()
        return Response({'whitelabels': queryset})



# Add Bloqueio de URL - By BILL
@user_passes_test(lambda u: u.groups.filter(name='visitante').count() == 0, login_url='/whitelabels/deny/')
@user_passes_test(lambda u: u.groups.filter(name='analista').count() == 0,  login_url='/whitelabels/deny/')
@user_passes_test(lambda u: u.groups.filter(name='dpo').count() == 0, login_url='/whitelabels/deny/')
def add_whitelabel_view(request):
    form = None

    if request.method == 'GET':
        form = WhitelabelForm()
    elif request.method == 'POST':
        form = WhitelabelForm(request.POST)
        if form.is_valid():
            whitelabel_args = {
            'site_name': form.cleaned_data['site_name'],
            'academy_link': form.cleaned_data['academy_link'],
            'browser_icon':  form.cleaned_data['browser_icon'],
            'interface_icon':  form.cleaned_data['interface_icon'],
            'interface_logo':  form.cleaned_data['interface_logo'],
            'report_logo':  form.cleaned_data['report_logo']
            }
            whitelabel = Whitelabel(**whitelabel_args)
            whitelabel.save()

            messages.success(request, 'Ativo aualizado com sucesso')
    #        return redirect('show_whitelabel_menu')


    return render(request, 'menu-whitelabel.html', {'form': form,  'whitelabel': whitelabel})




######################################  EDIT VIEW #################################


# Modificação - Risco quantitativo - "financeiro"

# Add Bloqueio de URL - By BILL
@user_passes_test(lambda u: u.groups.filter(name='visitante').count() == 0, login_url='/whitelabels/deny/')
@user_passes_test(lambda u: u.groups.filter(name='analista').count() == 0,  login_url='/whitelabels/deny/')
@user_passes_test(lambda u: u.groups.filter(name='dpo').count() == 0, login_url='/whitelabels/deny/')
def edit_whitelabel_view(request, whitelabel_id):
    whitelabel = get_object_or_404(Whitelabel, id=whitelabel_id)

    form = WhitelabelForm()
    if request.method == 'GET':
        form = WhitelabelForm(instance=whitelabel)
    elif request.method == 'POST':
        form = WhitelabelForm(request.POST, request.FILES, instance=whitelabel)
        if form.is_valid():
	    Whitelabel.objects.get(id=whitelabel_id)
            whitelabel.site_name = form.cleaned_data['site_name'].encode('utf-8')
            whitelabel.academy_link = form.cleaned_data['academy_link']
            whitelabel.browser_icon = form.cleaned_data['browser_icon']
            whitelabel.interface_icon = form.cleaned_data['interface_icon']
            whitelabel.interface_logo = form.cleaned_data['interface_logo']
            whitelabel.report_logo = form.cleaned_data['report_logo']
            whitelabel.save()

	    messages.success(request, 'Whitelabel aualizado com sucesso')

    return render(request, 'menu-whitelabel.html',  {'form': form, 'whitelabel': whitelabel})



