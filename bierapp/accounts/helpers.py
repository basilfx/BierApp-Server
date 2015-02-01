from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, Field
from crispy_forms.bootstrap import PrependedText, FormActions


class AuthenticationFormHelper(FormHelper):
    @property
    def layout(self):
        return Layout(
            PrependedText("username", "@"),
            PrependedText("password", "K"),
            Field("remember_me"),

            Div(
                Div(
                    Submit("login", _("Login"), css_class="btn-primary"),
                    css_class="controls"
                ),
                css_class="control-group"
            )
        )

    @property
    def form_class(self):
        return "form-horizontal"


class ChangePasswordFormHelper(FormHelper):
    @property
    def layout(self):
        return Layout(
            Field("password_current"),

            Field("password1"),
            Field("password2"),

            FormActions(
                Submit("submit", _("Change password"), css_class="btn-primary"),
            )
        )

    @property
    def form_class(self):
        return "form-horizontal"


class ChangeProfileFormHelper(FormHelper):
    @property
    def layout(self):
        return Layout(
            Field("first_name"),
            Field("last_name"),
            Field("birthdate"),
            Field("avatar"),

            FormActions(
                Submit("submit", _("Upload"), css_class="btn-primary"),
            )
        )

    @property
    def form_class(self):
        return "form-horizontal"


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

    @property
    def form_class(self):
        return "form-horizontal"


class ChooseSiteFormHelper(FormHelper):
    @property
    def layout(self):
        return Layout(
            Field("site"),

            FormActions(
                Submit("choose", _("Continue"), css_class="btn-primary"),
            )
        )

    @property
    def form_class(self):
        return "form-horizontal"


class SiteFormHelper(FormHelper):
    @property
    def layout(self):
        return Layout(
            Field("name"),

            FormActions(
                Submit("submit", _("Create"), css_class="btn-primary"),
            )
        )

    @property
    def form_class(self):
        return "form-horizontal"


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

    @property
    def form_class(self):
        return "form-horizontal"
