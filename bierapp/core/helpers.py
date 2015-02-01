from django.core.urlresolvers import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field, Fieldset
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions, InlineField

from crispy_forms_extra.layout import Tr, Td

class ProductGroupFormHelper(FormHelper):
    @property
    def layout(self):
        return Layout(
            Field('title'),
            Field('value'),
            Field('is_app_visible'),

            FormActions(
                Submit('submit', 'Add', css_class="btn-primary"),
            )
        )

class ProductFormHelper(FormHelper):
    @property
    def layout(self):
        return Layout(
            Field('title'),
            Field('value'),
            Field('is_app_visible'),

            FormActions(
                Submit('submit', 'Add', css_class="btn-primary"),
            )
        )

class TransactionFormHelper(FormHelper):
    @property
    def layout(self):
        return Layout(
            Field('description', css_class='input-xlarge'),
        )

    @property
    def form_tag(self):
        return False

class InlineTransactionItemFormHelper(FormHelper):
    @property
    def layout(self):
        return Tr(
            'id',
            Td(
                Field('product', template="bootstrap3/field_nolabel.html")
            ),
            Td(
                Field('count', template="bootstrap3/field_nolabel.html")
            ),
            Td(
                Field('DELETE', template="bootstrap3/field_nolabel.html")
            )
        )

    @property
    def form_tag(self):
        return False

    @property
    def help_text_inline(self):
        return False

class DummyFormHelper(FormHelper):
    @property
    def layout(self):
        return Layout(
            FormActions(
                Submit('submit', 'Add', css_class="btn-primary"),
            )
        )

    @property
    def form_tag(self):
        return False

class InviteGuestFormHelper(FormHelper):
    @property
    def layout(self):
        return Layout(
            Field('email'),

            FormActions(
                Submit('submit', 'Add', css_class="btn-primary"),
            )
        )

class PickTemplateFormHelper(FormHelper):
    @property
    def layout(self):
        return Layout(
            InlineField('template'),
            HTML("&nbsp;"),
            Submit('submit', 'Execute', css_class="btn-primary")
        )

    @property
    def form_class(self):
        return "form-inline"

    @property
    def form_method(self):
        return "GET"

    @property
    def form_action(self):
        return reverse("bierapp.core.views.transaction_create")

class ExportFormHelper(FormHelper):
    @property
    def layout(self):
        return Layout(
            Field('export_type'),
        )

    @property
    def form_class(self):
        return "form-horizontal"

    @property
    def form_method(self):
        return "GET"

class TransactionFilterHelper(FormHelper):
    @property
    def layout(self):
        return Layout(
            Field('after'),
            Field('before'),
            Field('description'),
            Field('product'),
            Field('accounted_user'),
            Field('executing_user'),
        )

    @property
    def form_class(self):
        return "form-horizontal"

    @property
    def form_method(self):
        return "GET"

class RangeFilterHelper(FormHelper):
    @property
    def layout(self):
        return Layout(
            Field('after'),
            Field('before'),
            Field('description'),
        )

    @property
    def form_class(self):
        return "form-horizontal"

    @property
    def form_method(self):
        return "GET"