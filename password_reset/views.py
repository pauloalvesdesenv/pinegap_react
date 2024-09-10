from django.shortcuts import render
from braces import views as bracesviews
from django.views import generic
from .forms import RegisterForm, LoginForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth import views as auth_views
from django.contrib.auth import authenticate, login, logout
from django.utils.translation import ugettext, ugettext_lazy as _
from django.urls import reverse_lazy
from django.contrib import auth
# Create your views here.

User = get_user_model()


(...)


class PasswordChangeView(auth_views.PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'templates/registration/password-change.html'
    success_url = reverse_lazy('home')
    form_valid_message = _("Your password was changed!")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class PasswordResetView(auth_views.PasswordResetView):
    form_class = PasswordResetForm
    template_name = 'templates/registration/password_reset.html'
    success_url = reverse_lazy('templates:password_reset_done')
    subject_template_name = 'templates/registration/password_reset_subject.txt'
    email_template_name = 'templates/registration/password_reset_email.txt'


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'templates/registration/password_reset_done.html'


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'templates/registration/password_reset_confirm.html'
    form_class = SetPasswordForm
    success_url = reverse_lazy('home')
    form_valid_message = _("Your password was changed!")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
