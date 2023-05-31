from django import forms
from django.contrib.admin.utils import help_text_for_field
from django.forms.widgets import Select


class SortForm(forms.Form):
    sort = forms.ChoiceField(help_text="Izaberite opciju", required=False)

    def clean_sort(self):
        data = self.cleaned_data['sort']
        return data


class FilterForm(forms.Form):
    # CHOICES = (('', "Izaberite opciju"),('1', 'bla'), ('Option 2', 'Option 2'),)
    field = forms.ChoiceField(choices=[], required=False, label='',
                              widget=forms.Select(attrs={'class':'selectpicker'}))
