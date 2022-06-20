from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group
from django.utils import timezone
from datetime import date, datetime
from django.contrib.auth.models import User

class Echo(models.Model):
    # number = models.AutoField(primary_key=True)
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, blank=True, null=True)
    group = models.ForeignKey(Group, models.SET_NULL, blank=True, null=True)
    type = models.CharField(max_length=16, default='self', blank=False, null=False)
    name = models.CharField(max_length=64, default=None, blank=False, null=False)
    description = models.TextField(default=None, blank=True, null=True)
    question = models.TextField(default=None, blank=False, null=False)
    created_at = models.DateTimeField(default=timezone.now, blank=True, null=True)

    class Meta:
        db_table = 'echoes'
        indexes = [
           models.Index(fields=['group']),
           models.Index(fields=['type'])
        ]

####################################################################

## Looks a bit like BaseIlluminator
class BaseEcho(models.Model):
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
    echo = models.ForeignKey(Echo, models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, blank=True, null=True)
    ## the number elements when input_keywords explodes. somewhat redundant but whatever
    input_count = models.IntegerField(default=0, blank=False, null=False)
    ## words joined by '|'
    input_keywords = models.CharField(max_length=256, default=None, blank=False, null=False)
    ## the answer as typed in by the user
    input_data = models.TextField(default=None, blank=True, null=True)

    class Meta:
        abstract = True
        indexes = [
           models.Index(fields=['echo'])
        ]

class SelfEcho(BaseEcho):

    class Meta:
        db_table = 'self_echo'

'''
class VoiceEcho(BaseEcho):

    class Meta:
        db_table = 'voice_echo'

class PlaceEcho(BaseEcho):

    class Meta:
        db_table = 'place_echo'

class EventEcho(BaseEcho):

    class Meta:
        db_table = 'event_echo'

class ObjectEcho(BaseEcho):

    class Meta:
        db_table = 'object_echo'

class PersonEcho(BaseEcho):
    dream_gender = models.CharField(max_length=16, default='male', blank=True)

    class Meta:
        db_table = 'person_echo'
'''
