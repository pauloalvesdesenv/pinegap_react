# -*- coding: utf-8 -*-
from django.shortcuts import render
# Global Whitelabel Reflected


from django.template import RequestContext #image
from django.db.models import Value, CharField, Case, When, Q, Count
from whitelabels.models import Brand
from django.http import JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from django.conf import settings # Upload Files
from django.http import HttpResponseRedirect

from whitelabels.models import Brand

# API VIEW WHITELABEL


class Get_Api(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'login.html'

    def whitelabel(self, request):
        queryset = Brand.objects.all()
        return Response({'whitelabels': queryset})


############# Generic View ###############




def show_whitelabel_base(request):
    whitelabels  = Brand.objects.all()
    return render(request, 'base.html', {
        'whitelabels': whitelabels
    })





def show_whitelabel_home(request):
    whitelabels  = Brand.objects.all()
    return render(request, 'home.html', {
        'whitelabels': whitelabels
    })




def show_whitelabel_login(request):
    whitelabels  = Brand.objects.all()
    return render(request, 'login.html', {
        'whitelabels': whitelabels
    })



