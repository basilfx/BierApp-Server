from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm as DjangoAuthenticationForm
from django import forms

from bierapp.accounts.models import User, UserMembershipInvite, Site
from bierapp.accounts.helpers import ChangePasswordFormHelper, ChangeProfileFormHelper, RegisterFormHelper, SiteFormHelper, UserMembershipInviteFormHelper, AuthenticationFormHelper, ChooseSiteFormHelper

import time


class AuthenticationForm(DjangoAuthenticationForm):
    remember_me = forms.BooleanField(required=False)

    helper = AuthenticationFormHelper()


class ChangePasswordForm(forms.ModelForm):
    error_messages = {
        "password_invalid": _("Current password does not match the old password."),
        "password_mismatch": _("The two password fields do not match."),
    }

    password_current = forms.CharField(label=_("Current password"), widget=forms.PasswordInput)
    password1 = forms.CharField(label=_("New password"), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("New password confirmation"), widget=forms.PasswordInput, help_text=_("Enter the same password as above, for verification."))

    helper = ChangePasswordFormHelper()

    class Meta:
        model = User
        fields = tuple()

    def clean_password_current(self):
        password_current = self.cleaned_data.get("password_current")

        if not self.instance.check_password(password_current):
            raise forms.ValidationError(self.error_messages["password_invalid"])

        return password_current

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages["password_mismatch"])

        return password2

    def save(self, commit=True):
        user = super(ChangePasswordForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password2"])

        if commit:
            user.save()

        return user


class ChangeProfileForm(forms.ModelForm):

    helper = ChangeProfileFormHelper()

    class Meta:
        model = User
        fields = ("first_name", "last_name", "birthdate", "avatar", )


class RegisterForm(forms.ModelForm):

    error_messages = {
        "duplicate_email": _("A user with that email address already exists."),
        "password_mismatch": _("The two password fields do not match."),
    }

    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"), widget=forms.PasswordInput, help_text=_("Enter the same password as above, for verification."))

    helper = RegisterFormHelper()

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")

    def clean_email(self):
        email = self.cleaned_data["email"]

        try:
            # Set small timeout to decrease number of requests per second
            time.sleep(0.100)

            # Find user
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email

        raise forms.ValidationError(self.error_messages["duplicate_email"])

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages["password_mismatch"])

        return password2

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password2"])

        if commit:
            user.save()

        return user


class ChooseSiteForm(forms.Form):
    site = forms.ModelChoiceField(queryset=Site.objects, empty_label=None)

    helper = ChooseSiteFormHelper()

    def __init__(self, sites, *args, **kwargs):
        super(ChooseSiteForm, self).__init__(*args, **kwargs)
        self.fields["site"].queryset = sites


class SiteForm(forms.ModelForm):
    helper = SiteFormHelper()

    class Meta:
        model = Site
        fields = ("name", )


class UserMembershipInviteForm(forms.ModelForm):
    helper = UserMembershipInviteFormHelper()

    def __init__(self, site, roles, *args, **kwargs):
        super(UserMembershipInviteForm, self).__init__(*args, **kwargs)

        self.site = site
        self.fields["role"].choices = roles

    def save(self, commit=True):
        instance = super(UserMembershipInviteForm, self).save(commit=False)
        instance.site = self.site

        if commit:
            instance.save()

        return instance

    class Meta:
        model = UserMembershipInvite
        fields = ("email", "role")
        widgets = {
            "role": forms.RadioSelect(),
        }