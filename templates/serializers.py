
from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings
from django.utils.translation import gettext as _
from rest_framework import serializers

####### Whitelabel Model #####
from whitelabels.models import Brand


###### IMPORT YOUR USER MODEL ######
from .models import ExampleUserModel

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password_reset_form_class = PasswordResetForm
    def validate_email(self, value):
        self.reset_form = self.password_reset_form_class(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(_('Error'))

        ###### FILTER YOUR USER MODEL ######
        if not ExampleUserModel.objects.filter(email=value).exists():

            raise serializers.ValidationError(_('Invalid e-mail address'))
        return value

    def save(self):
        request = self.context.get('request')
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),

            ###### USE YOUR TEXT FILE ######
            'email_template_name': 'password_reset_email.txt',

            'request': request,
        }
        self.reset_form.save(**opts)


# WHITELABEL  SERIALIZER #

class BrandSerializer(serializers.HyperlinkedModelSerializer):
    assets = serializers.HyperlinkedRelatedField(queryset=Brand.objects.using('db').all(), view_name='show_whitelabel_view', many=True)

    class Meta:
        model = Brand
        fields = ('site_name', 'academy_link', 'browser_icon', 'interface_icon', 'interface_logo', 'report_logo')


