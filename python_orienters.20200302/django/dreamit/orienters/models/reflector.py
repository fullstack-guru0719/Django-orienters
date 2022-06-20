from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import date, datetime

class Reflector(models.Model):
    # number = models.AutoField(primary_key=True)
    ## team
    # team_id = models.IntegerField(default=0, blank=False, null=False)
    type = models.CharField(max_length=16, default='self', blank=False, null=False)
    # self = models.CharField(max_length=32, default=None, blank=True, null=True)
    sself = models.CharField(max_length=32, default=None, blank=True, null=True)
    person1 = models.CharField(max_length=32, default=None, blank=True, null=True)
    person2 = models.CharField(max_length=32, default=None, blank=True, null=True)
    # user_id = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, blank=True, null=True)
    # dream_name = models.CharField(max_length=256, default=None, blank=True, null=True)
    # dream_description = models.TextField(default=None, blank=True, null=True)
    dream_space = models.TextField(default=None, blank=True, null=True)
    dream_date = models.DateTimeField(default=timezone.now, blank=True, null=True)
    # D_DreamTime = models.DateTimeField(default=datetime.now, blank=True)
    # D_DreamType = models.IntegerField(default=None, blank=True, null=True)
    # dream_team_id = models.IntegerField(default=None, blank=True, null=True)
    ## What is the next field for ?

    class Meta:
        db_table = 'reflectors'
        indexes = [
           models.Index(fields=['user']),
        ]

####################################################################
####################################################################

class BaseAspectDescription(models.Model):
    cadence = models.IntegerField(default=0, blank=False, null=False)
    archetype = models.IntegerField(default=0, blank=False, null=False)
    aspect = models.IntegerField(default=0, blank=False, null=False)
    image = models.CharField(max_length=64, default=None, blank=True, null=True)
    title_1 = models.CharField(max_length=256, default=None, blank=True, null=True)
    title_2 = models.CharField(max_length=256, default=None, blank=True, null=True)
    text_1 = models.TextField(default=None, blank=True, null=True)
    text_2 = models.TextField(default=None, blank=True, null=True)
    text_3 = models.TextField(default=None, blank=True, null=True)
    text_4 = models.TextField(default=None, blank=True, null=True)
    text_5 = models.TextField(default=None, blank=True, null=True)
    text_6 = models.TextField(default=None, blank=True, null=True)

    class Meta:
        abstract = True

####################################################################

class SelfSelfAspectDescriptionMale(BaseAspectDescription):

    class Meta:
        db_table = 'self_self_aspect_descriptions_male'

class SelfSelfAspectDescriptionFemale(BaseAspectDescription):

    class Meta:
        db_table = 'self_self_aspect_descriptions_female'

####################################################################

class SelfPersonAspectDescriptionMale(BaseAspectDescription):

    class Meta:
        db_table = 'self_person_aspect_descriptions_male'

class SelfPersonAspectDescriptionFemale(BaseAspectDescription):

    class Meta:
        db_table = 'self_person_aspect_descriptions_female'

####################################################################

class PersonSelfAspectDescriptionMale(BaseAspectDescription):

    class Meta:
        db_table = 'person_self_aspect_descriptions_male'

class PersonSelfAspectDescriptionFemale(BaseAspectDescription):

    class Meta:
        db_table = 'person_self_aspect_descriptions_female'

####################################################################

class PersonPersonAspectDescriptionMale(BaseAspectDescription):

    class Meta:
        db_table = 'person_person_aspect_descriptions_male'

class PersonPersonAspectDescriptionFemale(BaseAspectDescription):

    class Meta:
        db_table = 'person_person_aspect_descriptions_female'

####################################################################
