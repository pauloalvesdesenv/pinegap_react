# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm

############## USER TREE - BY Bill ###############
from django.contrib.auth.models import User, Group


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username", max_length=130,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'name': 'username', 'value': ''}))
    password = forms.CharField(
        label="Password", max_length=130,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 'name': 'password', 'value': ''}))

#class SignUpForm(UserCreationForm):
#    username = forms.CharField(max_length=130, required=False, help_text='Optional.')
#     first_name = forms.CharField(max_length=130, required=False, help_text='Optional.')
#     last_name = forms.CharField(max_length=130, required=False, help_text='Optional.')
#     email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')


class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email', help_text='Obrigatório')
    first_name = forms.CharField(max_length=130, required=False, label='Nome',  help_text='Obrigatório.')
    last_name = forms.CharField(max_length=130, required=False, label='Sobrenome', help_text='Obrigatório.')
    username = forms.CharField(max_length=130, required=True, label='Usuário', help_text='Obrigatório.')
    group = forms.ModelChoiceField(queryset=Group.objects.exclude(name='root'), required=True, label='Grupo', help_text='Obrigatório.')

    class Meta:
        model = User
        fields = ( 'username', 'first_name', 'last_name', 'email', 'group' )

#    def __init__(self, *args, **kwargs):
#        qs = kwargs.pop("group_qs")
#        super().__init__(*args, **kwargs)
#        self.fields["group"].queryset = qs

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        username = form.cleaned_data.get('username')
        user.first_name = self.cleaned_data['last_name'],
        user.last_name = self.cleaned_data['first_name'],
        user.email =  user.email = self.cleaned_data["email"],
        user.group =  self.cleaned_data["group"]
        if commit:
            user.save()
        return user

