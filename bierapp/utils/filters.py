from bierapp.utils.fields import GroupedModelChoiceField

import django_filters

class GroupedModelChoiceFilter(django_filters.ModelChoiceFilter):
    field_class = GroupedModelChoiceField