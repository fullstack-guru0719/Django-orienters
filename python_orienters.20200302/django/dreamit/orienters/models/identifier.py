from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import date, datetime
from django.contrib.auth.models import User

class Human(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=16, default='male', blank=True)

####################################################################

class BaseWord(models.Model):
    # number = models.AutoField(primary_key=True)
    word = models.CharField(max_length=64)

    class Meta:
        abstract = True

class SelfWord(BaseWord):

    class Meta:
        db_table = 'self_words'

class VoiceWord(BaseWord):

    class Meta:
        db_table = 'voice_words'

class PlaceWord(BaseWord):

    class Meta:
        db_table = 'place_words'

class EventWord(BaseWord):

    class Meta:
        db_table = 'event_words'

class ObjectWord(BaseWord):

    class Meta:
        db_table = 'object_words'

class PersonWord(BaseWord):

    class Meta:
        db_table = 'person_words'

####################################################################

class BaseIdentifier(models.Model):
    # number = models.AutoField(primary_key=True)
    word_01 = models.IntegerField(default=None, blank=True, null=True)
    word_02 = models.IntegerField(default=None, blank=True, null=True)
    word_03 = models.IntegerField(default=None, blank=True, null=True)
    word_04 = models.IntegerField(default=None, blank=True, null=True)
    word_05 = models.IntegerField(default=None, blank=True, null=True)
    word_06 = models.IntegerField(default=None, blank=True, null=True)
    word_07 = models.IntegerField(default=None, blank=True, null=True)
    word_08 = models.IntegerField(default=None, blank=True, null=True)
    word_09 = models.IntegerField(default=None, blank=True, null=True)
    word_10 = models.IntegerField(default=None, blank=True, null=True)
    word_11 = models.IntegerField(default=None, blank=True, null=True)
    word_12 = models.IntegerField(default=None, blank=True, null=True)
    # user_id = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, blank=True, null=True)
    dream_name = models.CharField(max_length=256, default=None, blank=True, null=True)
    dream_description = models.TextField(default=None, blank=True, null=True)
    dream_space = models.TextField(default=None, blank=True, null=True)
    dream_date = models.DateTimeField(default=timezone.now, blank=True, null=True)
    # D_DreamTime = models.DateTimeField(default=datetime.now, blank=True)
    # D_DreamType = models.IntegerField(default=None, blank=True, null=True)
    # dream_team_id = models.IntegerField(default=None, blank=True, null=True)

    class Meta:
        abstract = True
        indexes = [
           models.Index(fields=['user']),
        ]

class SelfIdentifier(BaseIdentifier):

    class Meta:
        db_table = 'self_identifier'

class VoiceIdentifier(BaseIdentifier):

    class Meta:
        db_table = 'voice_identifier'

class PlaceIdentifier(BaseIdentifier):

    class Meta:
        db_table = 'place_identifier'

class EventIdentifier(BaseIdentifier):

    class Meta:
        db_table = 'event_identifier'

class ObjectIdentifier(BaseIdentifier):

    class Meta:
        db_table = 'object_identifier'

class PersonIdentifier(BaseIdentifier):
    dream_gender = models.CharField(max_length=16, default='male', blank=True)

    class Meta:
        db_table = 'person_identifier'

####################################################################
####################################################################

class ReportShare(models.Model):
    # number = models.AutoField(primary_key=True)
    report_stage = models.CharField(max_length=16, default='identifier', blank=False, null=False)
    report_target = models.CharField(max_length=16, default='self', blank=False, null=False)
    report_id = models.IntegerField(default=None, blank=False, null=False)
    entity_type = models.CharField(max_length=8, default='group', blank=False, null=False)
    entity_id = models.IntegerField(default=None, blank=False, null=False)

    class Meta:
        db_table = 'report_shares'
        indexes = [
           models.Index(fields=['report_stage', 'report_target', 'report_id', 'entity_type']),
        ]

####################################################################
####################################################################

class ReportAnswer(models.Model):
    # number = models.AutoField(primary_key=True)
    report_stage = models.CharField(max_length=16, default='identifier', blank=False, null=False)
    report_target = models.CharField(max_length=16, default='self', blank=False, null=False)
    report_id = models.IntegerField(default=None, blank=False, null=False)
    cadence = models.CharField(max_length=16, default=None, blank=False, null=False)
    iindex = models.IntegerField(default=None, blank=False, null=False)
    text = models.TextField(default=None, blank=True, null=True)

    class Meta:
        db_table = 'report_answers'
        indexes = [
           models.Index(fields=['report_stage', 'report_target', 'report_id', 'cadence', 'iindex']),
        ]

####################################################################
####################################################################

class BaseDescription(models.Model):
    archetype = models.CharField(max_length=64, default=None, blank=True, null=True)
    cadence = models.CharField(max_length=64, default=None, blank=True, null=True)
    title = models.CharField(max_length=256, default=None, blank=True, null=True)
    tagline = models.TextField(default=None, blank=True, null=True)
    report = models.TextField(default=None, blank=True, null=True)
    questions = models.TextField(default=None, blank=True, null=True)

    class Meta:
        abstract = True

####################################################################

class SelfDescriptionMale(BaseDescription):

    class Meta:
        db_table = 'self_descriptions_male'

class SelfDescriptionFemale(BaseDescription):

    class Meta:
        db_table = 'self_descriptions_female'

####################################################################

class VoiceDescriptionMale(BaseDescription):

    class Meta:
        db_table = 'voice_descriptions_male'

class VoiceDescriptionFemale(BaseDescription):

    class Meta:
        db_table = 'voice_descriptions_female'

####################################################################

class PlaceDescriptionMale(BaseDescription):

    class Meta:
        db_table = 'place_descriptions_male'

class PlaceDescriptionFemale(BaseDescription):

    class Meta:
        db_table = 'place_descriptions_female'

####################################################################

class EventDescriptionMale(BaseDescription):

    class Meta:
        db_table = 'event_descriptions_male'

class EventDescriptionFemale(BaseDescription):

    class Meta:
        db_table = 'event_descriptions_female'

####################################################################

class ObjectDescriptionMale(BaseDescription):

    class Meta:
        db_table = 'object_descriptions_male'

class ObjectDescriptionFemale(BaseDescription):

    class Meta:
        db_table = 'object_descriptions_female'

####################################################################

class PersonDescriptionMale(BaseDescription):

    class Meta:
        db_table = 'person_descriptions_male'

class PersonDescriptionFemale(BaseDescription):

    class Meta:
        db_table = 'person_descriptions_female'

####################################################################
####################################################################

## Was a waste of time doing this properly when a form submission
## didn't update as expected but instead keeps creating new records :P
class PdfPage(models.Model):
    stage = models.CharField(max_length=32)
    target = models.CharField(max_length=32)
    title_1 = models.CharField(max_length=256, default=None, blank=True, null=True)
    title_2 = models.CharField(max_length=256, default=None, blank=True, null=True)
    title_3 = models.CharField(max_length=256, default=None, blank=True, null=True)
    title_4 = models.CharField(max_length=256, default=None, blank=True, null=True)
    title_5 = models.CharField(max_length=256, default=None, blank=True, null=True)
    page_1 = models.TextField(default=None, blank=True, null=True)
    page_2 = models.TextField(default=None, blank=True, null=True)
    page_3 = models.TextField(default=None, blank=True, null=True)
    page_4 = models.TextField(default=None, blank=True, null=True)
    page_5 = models.TextField(default=None, blank=True, null=True)

    class Meta:
        db_table = 'pdf_pages'
