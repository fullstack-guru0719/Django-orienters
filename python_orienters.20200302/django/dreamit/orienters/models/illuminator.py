from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import date, datetime
from django.contrib.auth.models import User

class IlluminatorWord(models.Model):
    # number = models.AutoField(primary_key=True)
    word = models.CharField(max_length=64, blank=False, null=False)
    quality = models.IntegerField(default=0, blank=False, null=False)

    class Meta:
        db_table = 'illuminator_words'

####################################################################

class BaseIlluminator(models.Model):
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
    ## 1=text,2=sound,3=image,4=video
    input_type = models.IntegerField(default=1, blank=False, null=False)
    ## 1=embed,2=link,3=upload
    input_method = models.IntegerField(default=1, blank=False, null=False)
    ## the number elements when input_keywords explodes. somewhat redundant but whatever
    input_count = models.IntegerField(default=0, blank=False, null=False)
    ## words joined by '|'
    input_keywords = models.CharField(max_length=256, default=None, blank=False, null=False)
    ## the raw text as typed by the user
    input_data = models.TextField(default=None, blank=True, null=True)

    class Meta:
        abstract = True
        indexes = [
           models.Index(fields=['user']),
        ]

class SelfIlluminator(BaseIlluminator):

    class Meta:
        db_table = 'self_illuminator'

class VoiceIlluminator(BaseIlluminator):

    class Meta:
        db_table = 'voice_illuminator'

class PlaceIlluminator(BaseIlluminator):

    class Meta:
        db_table = 'place_illuminator'

class EventIlluminator(BaseIlluminator):

    class Meta:
        db_table = 'event_illuminator'

class ObjectIlluminator(BaseIlluminator):

    class Meta:
        db_table = 'object_illuminator'

class PersonIlluminator(BaseIlluminator):
    dream_gender = models.CharField(max_length=16, default='male', blank=True)

    class Meta:
        db_table = 'person_illuminator'
