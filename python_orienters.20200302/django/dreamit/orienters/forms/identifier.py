from django import forms
from django.forms import ModelForm, TextInput, HiddenInput, RadioSelect
from .. import models
from ..konstants import gender_choices

class BaseIdentifierForm(ModelForm):
    class Meta:
        model = models.BaseIdentifier
        fields = ['dream_name', 'dream_description']
        widgets = {
            'dream_name': forms.TextInput(attrs={'required': True}),
            'dream_description': forms.TextInput(attrs={'required': True}),
        }
        labels = {
            'dream_name': 'Enter the base-perception that you are orienting yourself to',
            'dream_description': 'Enter a short description to provide some context',
        }

    # Extra field not in model.
    # This is a string which consists of a comma separated list of integers
    words = forms.CharField(widget=forms.HiddenInput(), required=False)

class SelfIdentifierForm(BaseIdentifierForm):
    class Meta(BaseIdentifierForm):
        model = models.SelfIdentifier
        ## Why are these necessary when I've already inherited this class ?
        # fields = ['dream_name', 'dream_description']
        fields = BaseIdentifierForm.Meta.fields
        # BaseIdentifierForm.Meta.labels['dream_name'] = 'Enter the self-perception that you are orienting yourself to'
        labels = BaseIdentifierForm.Meta.labels
        labels['dream_name'] = 'Enter the self-perception that you are orienting yourself to'

class VoiceIdentifierForm(BaseIdentifierForm):
    class Meta(BaseIdentifierForm):
        model = models.VoiceIdentifier
        fields = BaseIdentifierForm.Meta.fields
        labels = BaseIdentifierForm.Meta.labels
        labels['dream_name'] = 'Enter the name of the voice that you are orienting yourself to'

class PlaceIdentifierForm(BaseIdentifierForm):
    class Meta(BaseIdentifierForm):
        model = models.PlaceIdentifier
        fields = BaseIdentifierForm.Meta.fields
        labels = BaseIdentifierForm.Meta.labels
        labels['dream_name'] = 'Enter the name of the place that you are orienting yourself to'

class EventIdentifierForm(BaseIdentifierForm):
    class Meta(BaseIdentifierForm):
        model = models.EventIdentifier
        fields = BaseIdentifierForm.Meta.fields
        labels = BaseIdentifierForm.Meta.labels
        labels['dream_name'] = 'Enter the name of the event that you are orienting yourself to'

class ObjectIdentifierForm(BaseIdentifierForm):
    class Meta(BaseIdentifierForm):
        model = models.ObjectIdentifier
        fields = BaseIdentifierForm.Meta.fields
        labels = BaseIdentifierForm.Meta.labels
        labels['dream_name'] = 'Enter the name of the object that you are orienting yourself to'

'''
# A failed attempt at form inheritance whereby
# dream_gender gets displayed but never saved properly :(

class PersonIdentifierForm(BaseIdentifierForm):
    class Meta(BaseIdentifierForm):
        model = models.PersonIdentifier
        fields = BaseIdentifierForm.Meta.fields
        ## Next line crashes django :)
        # fields.append('dream_gender')
        labels = BaseIdentifierForm.Meta.labels
        labels['dream_name'] = 'Enter the name of the person who you are orienting yourself to'

    ## Including this under widgets above will make it not appear on the browser.
    ## This field has a default value of 'male'
    dream_gender = forms.ChoiceField(
        label='Select the gender of the person',
        choices=gender_choices,
        widget=forms.RadioSelect,
        required=True,
        initial=gender_choices[0][0])
'''

class PersonIdentifierForm(ModelForm):
    class Meta:
        model = models.PersonIdentifier
        fields = ['dream_name', 'dream_description', 'dream_gender']
        widgets = {
            'dream_name': forms.TextInput(attrs={'required': True}),
            'dream_description': forms.TextInput(attrs={'required': True}),
        }
        labels = {
            'dream_name': 'Enter the name of the person who you are orienting yourself to',
            'dream_description': 'Enter a short description to provide some context',
            ## KO
            # 'dream_gender': 'Select the gender of the person',
        }

    ## Including this under widgets above will make it not appear on the browser.
    ## This field has a default value of 'male'
    dream_gender = forms.ChoiceField(
        label='Select the gender of the person',
        choices=gender_choices,
        widget=forms.RadioSelect,
        required=True,
        initial=gender_choices[0][0])

    # Extra field not in model.
    # This is a string which consists of a comma separated list of integers
    words = forms.CharField(widget=forms.HiddenInput(), required=False)

class PdfPageForm(ModelForm):
    class Meta:
        model = models.PdfPage
        fields = ['id', 'stage', 'target', 'title_1', 'page_1', 'title_2', 'page_2', 'title_3', 'page_3', 'title_4', 'page_4', 'title_5', 'page_5']
