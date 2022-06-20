from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group
from django.utils import timezone
from datetime import date, datetime
from django.contrib.auth.models import User

class Connector(models.Model):
    # number = models.AutoField(primary_key=True)
    ## team
    # team_id = models.IntegerField(default=0, blank=False, null=False)
    group = models.ForeignKey(Group, models.SET_NULL, blank=True, null=True)
    ## usersdata
    # user_data = models.TextField(default=None, blank=True, null=True)
    ## connectorType
    type = models.CharField(max_length=16, default='group', blank=False, null=False)
    ## connectorCadence
    cadence = models.CharField(max_length=16, default=None, blank=True, null=True)
    ## connectorCadenceMax
    cadence_max = models.IntegerField(default=None, blank=True, null=True)
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
    ## Say if a connector (of type cadence) has cadence 'assert' and id 200.
    ## Then, a connector (of type cadence) with cadence 'organise' and id 210
    ## which was created from the detail page of 200 will have source = 200.
    ## Moreover, a connector (of type cadence) with cadence 'think' and id 220
    ## which was created from the detail page of 210 will have source = 200, not 210.
    source = models.IntegerField(default=None, blank=True, null=True)

    class Meta:
        db_table = 'connectors'
        indexes = [
           models.Index(fields=['user']),
        ]

## This table does not exists in the old one
class ConnectorReport(models.Model):
    # number = models.AutoField(primary_key=True)
    connector = models.ForeignKey(Connector, models.SET_NULL, blank=True, null=True, related_name='repz')
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, blank=True, null=True)
    stage = models.CharField(max_length=32)
    target = models.CharField(max_length=32)
    report_id = models.IntegerField(default=0, blank=False, null=False)

    class Meta:
        db_table = 'connector_reports'
