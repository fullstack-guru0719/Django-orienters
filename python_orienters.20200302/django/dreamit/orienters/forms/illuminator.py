from django import forms
from django.forms import ModelForm
# , TextInput, HiddenInput, RadioSelect
from .. import models
from ..konstants import gender_choices, input_type_choices

class BaseIlluminatorForm(ModelForm):
    class Meta:
        model = models.BaseIlluminator
        # 'input_count' isn't really necessary in Python
        fields = ['dream_name', 'dream_description', 'input_type', 'input_method', 'input_data', 'input_keywords']
        widgets = {
            'dream_name': forms.TextInput(attrs={'required': True}),
            'dream_description': forms.TextInput(attrs={'required': True}),
            'input_type': forms.HiddenInput(),
            'input_method': forms.HiddenInput(),
            'input_data': forms.HiddenInput(),
            'input_keywords': forms.HiddenInput(),
            ## Do I need this ?
            # 'input_count': forms.HiddenInput(),
        }
        labels = {
            'dream_name': 'Enter the base-perception that you are orienting yourself to',
            'dream_description': 'Enter a short description to provide some context',
            'input_type': 'To illuminate an artefact, either embed link or upload it by using the radio buttons'
        }

    '''
    input_type = forms.ChoiceField(
        label='To illuminate an artefact, either embed link or upload it by using the radio buttons',
        choices=input_type_choices,
        widget=forms.RadioSelect,
        required=True,
        initial=input_type_choices[0][0])
    '''

class SelfIlluminatorForm(BaseIlluminatorForm):
    class Meta(BaseIlluminatorForm.Meta):
        model = models.SelfIlluminator
        ## Why are these necessary when I've already inherited this class ?
        # fields = BaseIlluminatorForm.Meta.fields
        # BaseIlluminatorForm.Meta.labels['dream_name'] = 'Enter the self-perception that you are orienting yourself to'
        labels = BaseIlluminatorForm.Meta.labels
        labels['dream_name'] = 'Enter the self-perception that you are orienting yourself to'

class VoiceIlluminatorForm(BaseIlluminatorForm):
    class Meta(BaseIlluminatorForm.Meta):
        model = models.VoiceIlluminator
        # fields = BaseIlluminatorForm.Meta.fields
        labels = BaseIlluminatorForm.Meta.labels
        labels['dream_name'] = 'Enter the name of the voice that you are orienting yourself to'

class PlaceIlluminatorForm(BaseIlluminatorForm):
    class Meta(BaseIlluminatorForm.Meta):
        model = models.PlaceIlluminator
        # fields = BaseIlluminatorForm.Meta.fields
        labels = BaseIlluminatorForm.Meta.labels
        labels['dream_name'] = 'Enter the name of the place that you are orienting yourself to'

class EventIlluminatorForm(BaseIlluminatorForm):
    class Meta(BaseIlluminatorForm.Meta):
        model = models.EventIlluminator
        # fields = BaseIlluminatorForm.Meta.fields
        labels = BaseIlluminatorForm.Meta.labels
        labels['dream_name'] = 'Enter the name of the event that you are orienting yourself to'

class ObjectIlluminatorForm(BaseIlluminatorForm):
    class Meta(BaseIlluminatorForm.Meta):
        model = models.ObjectIlluminator
        # fields = BaseIlluminatorForm.Meta.fields
        labels = BaseIlluminatorForm.Meta.labels
        labels['dream_name'] = 'Enter the name of the object that you are orienting yourself to'

class PersonIlluminatorForm(BaseIlluminatorForm):
    class Meta(BaseIlluminatorForm.Meta):
        model = models.PersonIlluminator
        fields = ['dream_name', 'dream_description', 'dream_gender', 'input_type', 'input_method', 'input_data', 'input_keywords']

    ## Including this under widgets above will make it not appear on the browser.
    ## This field has a default value of 'male'
    dream_gender = forms.ChoiceField(
        label='Select the gender of the person',
        choices=gender_choices,
        widget=forms.RadioSelect,
        required=True,
        initial=gender_choices[0][0])
