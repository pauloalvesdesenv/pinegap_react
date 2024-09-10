
# -*- coding: utf-8 -*-

from rest_framework import serializers
from .models import Brand




class BrandSerializer(serializers.HyperlinkedModelSerializer):
    assets = serializers.HyperlinkedRelatedField(queryset=Brand.objects.using('db').all(), view_name='show_whitelabel_view', many=True)

    class Meta:
        model = Brand
        fields = ('site_name', 'academy_link', 'browser_icon', 'interface_icon', 'interface_logo', 'report_logo')





