# -*- coding: utf-8 -*-
"""View and API definitions for Settings."""

from django.db.models.fields import files
from json import JSONEncoder

#from . import serializers
from rest_framework import serializers

from . import serializers
from django.shortcuts import redirect
from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib import messages
from django.db.models import Value, CharField, Q #Billing
from django.forms.models import model_to_dict #Billing
from django.utils.encoding import smart_str #Billing
from django.http import JsonResponse, HttpResponse, QueryDict #Billing
from django.utils import timezone as tz #Billing
from django.views.decorators.csrf import csrf_exempt #Billing
#from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
#from . models import Whitelabel
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import csv
import os               #Billing
import mimetypes        #Billing
import datetime         #Billing
import urllib           #Billing
import json             #Billing

#tst
#from rest_framework import viewsets
from whitelabels.serializers import BrandSerializer
#from whitelabels.models import Whitelabel
from .models import Brand

#from django.http import JsonResponse

#from django.forms.models import model_to_dict
#from rest_framework.decorators import api_view






# GET WHITELABEL JSON REST API
@api_view(['GET'])
def whitelabel_api(request):
    """List Events."""
    brands = []
    for e in Brand.objects.all().order_by('-id')[:100]:
        brands.append(model_to_dict(e))

    return JsonResponse(brands, json_dumps_params={'indent': 2}, safe=False)

