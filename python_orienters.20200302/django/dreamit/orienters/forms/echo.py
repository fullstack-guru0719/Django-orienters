from django import forms
from django.contrib.auth.models import Group, User
from django.forms import ModelForm
# , TextInput, HiddenInput, RadioSelect
from .. import models

class EchoForm(ModelForm):
    ## Doesn't display as a proper multiple select drop down at all
    # group = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), widget=forms.CheckboxSelectMultiple(), initial=1)

    class Meta:
        model = models.Echo
        fields = ['id', 'group', 'type', 'name', 'description', 'question']
