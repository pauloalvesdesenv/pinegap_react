# -*- coding: utf-8 -*-
"""View and API definitions for Settings."""

from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from .models import Setting
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import csv

###################### 	 WHITELABEL BY BILL #################

from django.db.models.fields import files
from json import JSONEncoder
from rest_framework import serializers
#from .import serializers
from django.shortcuts import redirect
from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib import messages
from django.db.models import Value, CharField, Q #Billing
from django.forms.models import model_to_dict #Billing
from django.utils.encoding import smart_str #Billing
from django.http import JsonResponse, HttpResponse, QueryDict #Billing
from django.utils import timezone as tz #Billing
from django.views.decorators.csrf import csrf_exempt #Billing
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import csv
import os               #Billing
import mimetypes        #Billing
import datetime         #Billing
import urllib           #Billing
import json             #Billing

#
from whitelabels.serializers import BrandSerializer
from whitelabels.models import Brand

############################################################







@api_view(['POST'])
def update_setting_api(request):
    """API: Update a setting value."""
    setting_id = request.data["setting_id"]
    setting = get_object_or_404(Setting, id=setting_id)
    setting.value = request.data["setting_value"]
    setting.save(force_update=True)
    messages.success(request, 'Setting successfully updated!')

    return JsonResponse({'status': 'success'})


@api_view(['POST'])
def add_setting_api(request):
    """API: Add a setting key/value."""
    setting_key = request.data["setting_key"]
    if Setting.objects.filter(key=setting_key).count() == 0:
        new_settings_args = {
            "key": request.data["setting_key"],
            "value": request.data["setting_value"],
            "comments": "n/a",
        }
        new_setting = Setting.objects.create(**new_settings_args)
        new_setting.save()

        messages.success(request, 'Setting successfully updated!')
        return JsonResponse({'status': 'success'})

    return JsonResponse(data={'status': 'error'}, status=403)


@api_view(['GET'])
def delete_setting_api(request, setting_id):
    """API: Delete a setting key/value."""
    setting = get_object_or_404(Setting, id=setting_id)
    setting.delete()
    messages.success(request, 'Setting successfully deleted!')

    return JsonResponse({'status': 'success'})


@api_view(['GET'])
def export_settings_api(request):
    """API: Export settings."""
    response = HttpResponse(content_type='text/csv')
    filename = "pinegap_settings.csv"
    response['Content-Disposition'] = 'attachment; filename=' + filename
    writer = csv.writer(response, delimiter=';')

    settings = Setting.objects.all()

    writer.writerow(['keys', 'values'])  # headers
    for setting in settings:
        writer.writerow([setting.key, setting.value, setting.comments])

    return response


@api_view(['GET'])
def import_settings_api(request):
    """API: Export settings."""
    # @Todo
    pass

@api_view(['GET'])
def user_details_api(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return JsonResponse(user, safe=False)

@api_view(['GET'])
def delete_user_api(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return JsonResponse({'status': 'deleted'})



@api_view(['GET'])
def get_api(request):
    """Get Whitelabel Records."""
    brands = []
    for e in Brand.objects.all().order_by('-id')[:100]:
        brands.append(model_to_dict(e))

    return JsonResponse(brands, json_dumps_params={'indent': 2}, safe=False)




