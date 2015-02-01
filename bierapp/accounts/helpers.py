from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, Field
from crispy_forms.bootstrap import PrependedText, FormActions


class AuthenticationFormHelper(FormHelper):
    @property
    def layout(self):
        return Layout(
            PrependedText('username', '@'),
            PrependedText('password', 'K'),
            Field('remember_me'),

            Div(
                Div(
                    Submit('login', 'Login', css_class="btn-primary"),
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
            Field('password_current'),

            Field('password1'),
            Field('password2'),

            FormActions(
                Submit('submit', 'Change password', css_class="btn-primary"),
            )
        )

    @property
    def form_class(self):
        return "form-horizontal"


class ChangeProfileFormHelper(FormHelper):
    @property
    def layout(self):
        return Layout(
            Field('avatar'),

            FormActions(
                Submit('submit', 'Upload', css_class="btn-primary"),
            )
        )

    @property
    def form_class(self):
        return "form-horizontal"


class RegisterFormHelper(FormHelper):
    @property
    def layout(self):
        return Layout(
            Field('email'),
            Field('first_name'),
            Field('last_name'),

            Field('password1'),
            Field('password2'),

            FormActions(
                Submit('register', 'Register', css_class="btn-primary"),
            )
        )

    @property
    def form_class(self):
        return "form-horizontal"


class ChooseSiteFormHelper(FormHelper):
    @property
    def layout(self):
        return Layout(
            Field('site'),

            FormActions(
                Submit('choose', 'Continue', css_class="btn-primary"),
            )
        )

    @property
    def form_class(self):
        return "form-horizontal"


class SiteFormHelper(FormHelper):
    @property
    def layout(self):
        return Layout(
            Field('name'),

            FormActions(
                Submit('submit', 'Create', css_class="btn-primary"),
            )
        )

    @property
    def form_class(self):
        return "form-horizontal"


class UserMembershipInviteFormHelper(FormHelper):
    @property
    def layout(self):
        return Layout(
            Field('email'),

            FormActions(
                Submit('submit', 'Invite', css_class="btn-primary"),
            )
        )

    @property
    def form_class(self):
        return "form-horizontal"
