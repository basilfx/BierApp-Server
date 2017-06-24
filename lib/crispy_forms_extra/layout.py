from crispy_forms.utils import render_field
from django.template.loader import render_to_string

from crispy_forms.layout import TEMPLATE_PACK


class BaseTable(object):
    template = "%s/table_elements.html" % TEMPLATE_PACK

    def __init__(self, *fields, **kwargs):
        self.fields = fields

        if hasattr(self, "css_class") and "css_class" in kwargs:
            self.css_class += " %s" % kwargs.get("css_class")
        if not hasattr(self, "css_class"):
            self.css_class = kwargs.get("css_class", None)

        self.css_id = kwargs.get("css_id", "")
        self.template = kwargs.get("template", self.template)

    def render(self, form, form_style, context, template_pack):
        fields = ""

        for field in self.fields:
            fields += render_field(field, form, form_style, context)

        return render_to_string(self.template, {
            "tag": self.element,
            "element": self,
            "fields": fields})


class Td(BaseTable):
    element = "td"


class Tr(BaseTable):
    element = "tr"
