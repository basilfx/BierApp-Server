from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, Field
from crispy_forms.bootstrap import FormActions


class AuthenticationFormHelper(FormHelper):
    @property
    def layout(self):
        return Layout(
            Field("username"),
            Field("password"),
            Field("remember_me"),

            Div(
                Div(
                    Submit("login", _("Login"), css_class="btn-primary"),
                    css_class="controls"
                ),
                css_class="control-group"
            )
        )


class ChangePasswordFormHelper(FormHelper):
    @property
    def layout(self):
        return Layout(
            Field("password_current"),

            Field("password1"),
            Field("password2"),

            FormActions(
                Submit(
                    "submit", _("Change password"), css_class="btn-primary"),
            )
        )


class ChangeProfileFormHelper(FormHelper):
    @property
    def layout(self):
        return Layout(
            Field("first_name"),
            Field("last_name"),
            Field("birthdate", css_class="datepicker"),
            Field("avatar"),

            FormActions(
                Submit("submit", _("Upload"), css_class="btn-primary")
            )
        )


class RegisterFormHelper(FormHelper):
    @property
    def layout(self):
        return Layout(
            Field("email"),
            Field("first_name"),
            Field("last_name"),

            Field("password1"),
            Field("password2"),

            FormActions(
                Submit("register", _("Register"), css_class="btn-primary"),
            )
        )


class ChooseSiteFormHelper(FormHelper):
    @property
    def layout(self):
        return Layout(
            Field("site"),

            FormActions(
                Submit("choose", _("Continue"), css_class="btn-primary"),
            )
        )


class SiteFormHelper(FormHelper):
    @property
    def layout(self):
        return Layout(
            Field("name"),

            FormActions(
                Submit("submit", _("Create"), css_class="btn-primary"),
            )
        )


class UserMembershipInviteFormHelper(FormHelper):
    @property
    def layout(self):
        return Layout(
            Field("email"),
            Field("role"),

            FormActions(
                Submit("submit", _("Invite"), css_class="btn-primary"),
            )
        )


class UserMembershipFormHelper(FormHelper):
    @property
    def layout(self):
        return Layout(
            Field("role"),

            FormActions(
                Submit("submit", _("Save"), css_class="btn-primary"),
            )
        )
