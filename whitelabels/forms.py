from __future__ import unicode_literals
from django import forms
#from .models import settings
from .models import Whitelabel
from django.forms import ModelForm
from .models import Brand



class WhitelabelForm(forms.ModelForm):
    class Meta:
        model = Whitelabel
        fields = ['id', 'site_name', 'academy_link', 'browser_icon', 'interface_icon', 'interface_logo', 'report_logo']
        widgets = {
            'id': forms.HiddenInput(),
            'site_name': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'academy_link': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'browser_icon': forms.FileInput(attrs={'class': 'form-control form-control-sm'}),
            'interface_icon': forms.FileInput(attrs={'class': 'form-control form-control-sm'}),
            'interface_logo': forms.FileInput(attrs={'class': 'form-control form-control-sm'}),
            'report_logo': forms.FileInput(attrs={'class': 'form-control form-control-sm'})
        }

    def __init__(self, *args, **kwargs):
        super(WhitelabelForm, self).__init__(*args, **kwargs)

	id = [(whitelabel.id) for whitelabel in Brand.objects.all()]



