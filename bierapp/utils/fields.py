from django import forms
from django.forms import models

from itertools import groupby


class GroupedModelChoiceField(forms.ModelChoiceField):
    def __init__(self, queryset, group_by_field, group_label=None,
                 *args, **kwargs):
        """
        group_by_field is the name of a field on the model
        group_label is a function to return a label for each choice group
        """
        super(GroupedModelChoiceField, self).__init__(
            queryset, *args, **kwargs)
        self.group_by_field = group_by_field

        if group_label is None:
            self.group_label = lambda group: group
        elif type(group_label) == dict:
            self.group_label = lambda group: group_label[group]
        else:
            self.group_label = group_label

    def _get_choices(self):
        """
        Exactly as per ModelChoiceField except returns new iterator class
        """
        if hasattr(self, "_choices"):
            return self._choices
        return GroupedModelChoiceIterator(self)
    choices = property(_get_choices, forms.ModelChoiceField._set_choices)


class GroupedModelChoiceIterator(models.ModelChoiceIterator):
    def __iter__(self):
        if self.field.empty_label is not None:
            yield (u"", self.field.empty_label)

        groups = groupby(
            self.queryset.all(),
            key=lambda row: getattr(row, self.field.group_by_field))

        for group, choices in groups:
            yield (
                self.field.group_label(group),
                [self.choice(ch) for ch in choices]
            )
