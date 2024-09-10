# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect  #WL upl Fls
from django.contrib.auth.models import User
from django.db.models import F
from rest_framework.authtoken.models import Token
from .models import Setting
from events.models import Event
from users.views import user_details_view
import base64


# WHITELABEL DEPENDENCE - DONE BY BILL
from whitelabels.models import Brand
from whitelabels.views import whitelabel




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


def show_settings_menu(request):
    """View: List settings menus."""
    from cursor_pagination import CursorPaginator

    users = User.objects.exclude(username="admin", is_active="False").annotate(apitoken=F('auth_token'))
    settings = Setting.objects.all().order_by("key")
    events_list = Event.objects.all()

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

#    if request.method == 'POST' and request.FILES['myfile']:
#        myfile = request.FILES['myfile']
#        fs = FileSystemStorage()
#        filename = fs.save(myfile.name, myfile)
#        uploaded_file_url = fs.url(filename)

    return render(request, 'menu-settings.html', {
        'users': users,
        'settings': settings,
        'events': events,
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



