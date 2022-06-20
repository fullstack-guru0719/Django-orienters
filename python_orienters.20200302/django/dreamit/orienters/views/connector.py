import sys
import math

from random import randrange

from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.contrib.staticfiles import finders
from django.conf import settings
from django.shortcuts import render, redirect

# Create your views here.
from django.http import JsonResponse, HttpResponse, HttpResponseServerError

# from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict
from django.core.mail.message import EmailMessage

from django.core.paginator import Paginator

# from orienters.models import SelfWord, SelfIdentifier, SelfDescriptionMale, PersonWord, PersonIdentifier, PdfPage
# from orienters.models import *
from .. import models as M_O_D_E_L_S
from .. import forms

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from .. import konstants
# from .identifier import pdf, pdf_email, generate_pdf, generate_image_circle
from .identifier import generate_pdf, generate_image_circle

# importing get_template from loader
from django.template.loader import get_template

# import render_to_pdf from utils.py
from ..utils import render_to_pdf, get_gender, get_shared_report_ids, shared_reports_by_user

@login_required
def index(request):
    # 'connector/index' explodes into 'connector' & 'index'
    target, stage  = request.path.split('/')[-2:]

    user = request.user

    if request.method == 'POST':

        '''
        connector_type = request.POST.get('connector_type', 'fake')
        print("connector_type = " + connector_type, file=sys.stderr)

        ## Returned as a comma delimited string
        selected_reports = request.POST.getlist('selected_reports[]')
        for selected_report in selected_reports:
            print("selected_report => " + selected_report, file=sys.stderr)
        '''

        for key, values in request.POST.lists():
            print(key, values)

        ## Get relevant POST parameters
        group_id = request.POST.get('group_id')
        connector_type = request.POST.get('connector_type', 'group')
        cadence = request.POST.get('cadence')
        cadence_max = request.POST.get('cadence_max', None)

        ## Prep them for the model, just in case ...
        if not cadence_max:
            cadence_max = None

        if connector_type == 'group':
            cadence = None
            cadence_max = None

        reports = []
        for key, values in request.POST.lists():
            if key.startswith('user-'):
                # reports.append(values);
                reports.append(values[0]);

        print('DEBUG : reports =')
        for report in reports:
            print(report)

        group = Group.objects.get(id=group_id)

        ## Now, save the connector

        ## For cadence (i.e. connectorCadence), it might be set by whatever cadence button that was
        ## clicked as captured on line 300 in plugins/dreamit-core/js/common.js
        ## FYI, cadence is empty for connector_type 'group'

        ## For cadence_max (i.e. connectorCadenceMax), it might be set on a hidden input via Ajax
        ## on line 289 in plugins/dreamit-core/js/common.js
        ## and on line 148 in plugins/dreamit-core/dreamit-ajax.php
        ## FYI, cadence_max is empty or 0 for connector_type 'group'

        _c = M_O_D_E_L_S.Connector( \
            # group=group_id, \
            group=group, \
            type=connector_type, \
            cadence=cadence, \
            # cadence_max=randrange(0,12), \
            cadence_max=cadence_max, \
            user=user)
        _c.save()

        ## create child records
        for report in reports:
            # report_split = report[0].split('|')
            report_split = report.split('|')
            ## See the model definition for what 'repz' means
            _c.repz.create( \
                stage=report_split[0], \
                target=report_split[1], \
                report_id=report_split[2]
            )


        ## Construct return (redirect ?) url
        detail_url = target + '_' + 'detail'

        # return redirect(detail_url, id=new_record.id)
        return redirect(detail_url, id=_c.pk)
    ## end : if request.method == 'POST':

    groups = Group.objects.all()

    shared_report_ids = get_shared_report_ids('connector', None, user)

    # reports = M_O_D_E_L_S.Connector.objects.all().annotate(c_count=Count('repz')).order_by('-id')[:20]
    reports = M_O_D_E_L_S.Connector.objects.filter(\
        Q(user=user)\
        |Q(pk__in=shared_report_ids))\
        .annotate(c_count=Count('repz'))\
        .order_by('-id')[:20]

    paginator = Paginator(reports, konstants.records_per_page) # Show records_per_page results per page.

    page_number = request.GET.get('page', 1)
    reports_paginated = paginator.get_page(page_number)

    page_context = {
        'groups' : groups,
        'reports' : reports_paginated,
        'detail_url' : 'connector_detail'
    }

    return render(request, 'connector.html', page_context)

def reports_by_group(request, group_id):
    # username = request.GET.get('username', None)
    group = Group.objects.get(id=group_id)
    # users = group.user_set.all().values('id','first_name','last_name','username')
    users = group.user_set.all().only('id','first_name','last_name','username')

    # print('request.user.pk',request.user.pk)

    ## Get reports shared by each user
    uzzers = []
    for user in users:
        result = shared_reports_by_user(request, user)
        uzzers.append(result)
    ## end : for user in users

    data = {
        # 'users': list(users)
        'users': uzzers
    }
    return JsonResponse(data)

def calculate_cadence_max(request):
    print('calculate_cadence_max:')
    for key, values in request.POST.lists():
        print(key, values)

    reports = []
    for key, values in request.POST.lists():
        if key.startswith('user-'):
            # reports.append(values);
            reports.append(values[0]);

    ## Implement line 148 onwards in www/wp-content/plugins/dreamit-core/dreamit-ajax.php

    ## max possible value
    input_count = 12

    print('DEBUG : reports =')
    for report in reports:
        print(report)
        # report_split = report[0].split('|')
        # target,stage,report_id = report.split('|')
        stage,target,report_id = report.split('|')

        if stage == 'identifier':
            if target == 'self':
                report = M_O_D_E_L_S.SelfIdentifier.objects.get(pk=report_id)
            elif target == 'voice':
                report = M_O_D_E_L_S.VoiceIdentifier.objects.get(pk=report_id)
            elif target == 'place':
                report = M_O_D_E_L_S.PlaceIdentifier.objects.get(pk=report_id)
            elif target == 'event':
                report = M_O_D_E_L_S.EventIdentifier.objects.get(pk=report_id)
            elif target == 'object':
                report = M_O_D_E_L_S.ObjectIdentifier.objects.get(pk=report_id)
            elif target == 'person':
                report = M_O_D_E_L_S.PersonIdentifier.objects.get(pk=report_id)
            else:
                return HttpResponseServerError(stage + ' ' + target + ' is not supported')
            ## end : if target == 'self':

            _input_count = 12
            for x in range(1,13):
                word_field = 'word_{0:02d}'.format(x)
                word_field_value = getattr(report, word_field)
                if not word_field_value:
                    _input_count = x - 1
                    break

            if _input_count < input_count:
                input_count = _input_count
        ## end : if stage == 'identifier':

        if stage == 'illuminator':
            if target == 'self':
                report = M_O_D_E_L_S.SelfIlluminator.objects.get(pk=report_id)
            elif target == 'voice':
                report = M_O_D_E_L_S.VoiceIlluminator.objects.get(pk=report_id)
            elif target == 'place':
                report = M_O_D_E_L_S.PlaceIlluminator.objects.get(pk=report_id)
            elif target == 'event':
                report = M_O_D_E_L_S.EventIlluminator.objects.get(pk=report_id)
            elif target == 'object':
                report = M_O_D_E_L_S.ObjectIlluminator.objects.get(pk=report_id)
            elif target == 'person':
                report = M_O_D_E_L_S.PersonIlluminator.objects.get(pk=report_id)
            else:
                return HttpResponseServerError(stage + ' ' + target + ' is not supported')
            ## end : if target == 'self':

            if report.input_count < input_count:
                input_count = report.input_count
        ## end : if stage == 'illuminator':

    ## end : for report in reports:

    data = {
        # 'cadence_max': randrange(1,12)
        'cadence_max': input_count
    }
    return JsonResponse(data)

@login_required
def detail(request, id):
    # target, eyed = request.path.split('/')[-2:]
    stage, eyed = request.path.split('/')[-2:]

    print('id = ' + eyed)

    report = None
    patterns = None
    methods = None
    descriptions = []
    circle_data = {}
    image_name = None

    report = M_O_D_E_L_S.Connector.objects.get(pk=id)

    repz = report.repz.all()
    repz_count = repz.count()
    print('repz_count =',repz_count)

    group_name = report.group.name
    print('group_name =',group_name)

    ## Was this calculated back when we saved the connector ?
    ## Yes, as cadence_max, but for connectors with type 'group'
    ## cadence_max is deliberately set to 0. Why ? No idea ...
    input_count = 12

    user_name_report_title_list = []
    members = []

    connectors = []

    methods = konstants.connector_methods
    patterns = konstants.connector_patterns

    if report.type == 'cadence':
        cadence = report.cadence
        cadence_index = methods.index(cadence.capitalize())
        cadence_one_based_index = 1 if cadence_index == 0 else cadence_index

        print('~~~~~~~~~~ cadence =', cadence)
        print('cadence_one_based_index =', cadence_one_based_index)
    ## end : if report.type == 'cadence':

    for rep in repz:
        if rep.stage == 'identifier':
            if rep.target == 'self':
                _report = M_O_D_E_L_S.SelfIdentifier.objects.get(pk=rep.report_id)
            elif rep.target == 'voice':
                _report = M_O_D_E_L_S.VoiceIdentifier.objects.get(pk=rep.report_id)
            elif rep.target == 'place':
                _report = M_O_D_E_L_S.PlaceIdentifier.objects.get(pk=rep.report_id)
            elif rep.target == 'event':
                _report = M_O_D_E_L_S.EventIdentifier.objects.get(pk=rep.report_id)
            elif rep.target == 'object':
                _report = M_O_D_E_L_S.ObjectIdentifier.objects.get(pk=rep.report_id)
            elif rep.target == 'person':
                _report = M_O_D_E_L_S.PersonIdentifier.objects.get(pk=rep.report_id)
            else:
                return HttpResponseServerError(rep.stage + ' ' + rep.target + ' is not supported')
            ## end : if target == 'self':
        ## end : if stage == 'identifier':

        if rep.stage == 'illuminator':
            if rep.target == 'self':
                _report = M_O_D_E_L_S.SelfIlluminator.objects.get(pk=rep.report_id)
            elif rep.target == 'voice':
                _report = M_O_D_E_L_S.VoiceIlluminator.objects.get(pk=rep.report_id)
            elif rep.target == 'place':
                _report = M_O_D_E_L_S.PlaceIlluminator.objects.get(pk=rep.report_id)
            elif rep.target == 'event':
                _report = M_O_D_E_L_S.EventIlluminator.objects.get(pk=rep.report_id)
            elif rep.target == 'object':
                _report = M_O_D_E_L_S.ObjectIlluminator.objects.get(pk=rep.report_id)
            elif rep.target == 'person':
                _report = M_O_D_E_L_S.PersonIlluminator.objects.get(pk=rep.report_id)
            else:
                return HttpResponseServerError(rep.stage + ' ' + rep.target + ' is not supported')
            ## end : if target == 'self':
        ## end : if stage == 'illuminator':

        # user = User.objects.get(id=_report.user)
        user = _report.user
        members.append(user)

        ## Construct this ummm ... 'thing'
        connector = {}
        connector['user_id'] = user.id
        connector['arrey'] = make_array(_report)

        ## Get descriptions for each member
        if report.type == 'cadence':
            # archetype = patterns[connector['arrey'][cadence_one_based_index]]
            archetype = patterns[connector['arrey'][cadence_one_based_index - 1]]

            print('for user id', user.id)
            print('connector[\'arrey\'] =', connector['arrey'])
            print('connector[\'arrey\'][cadence_one_based_index - 1] =', connector['arrey'][cadence_one_based_index - 1])
            print('archetype =', archetype)
            print('cadence =', cadence.capitalize())

            ## first use the report user's gender
            gender = "male"
            if hasattr(user, 'human'):
                gender = user.human.gender

            ## if report has dream_gender, use that instead
            if hasattr(_report, 'dream_gender'):
                gender = _report.dream_gender

            if gender == 'male':
                # qs = M_O_D_E_L_S.PersonDescriptionMale.objects.filter(archetype=archetype, cadence=cadence)
                qs = M_O_D_E_L_S.PersonDescriptionMale.objects.filter(archetype=archetype, cadence=cadence.capitalize())
            else:
                qs = M_O_D_E_L_S.PersonDescriptionFemale.objects.filter(archetype=archetype, cadence=cadence.capitalize())
            # end : if gender == "male":

            q = qs[0]

            description = {}
            description['first_name'] = user.first_name
            description['title'] = q.title
            # description['report'] = q.report

            report_str_mod = q.report.replace('[name]', user.first_name)
            description['report'] = report_str_mod

            descriptions.append(description)
        # end : if report.type == 'cadence':

        connectors.append(connector)

        ## Was this calculated back when we saved the connector ?
        ## Yes, as cadence_max, but for connectors with type 'group'
        ## cadence_max is deliberately set to 0. Why ? No idea ...
        current_input_count = len(connector['arrey'])
        if current_input_count < input_count:
            input_count = current_input_count

        u_f_n_r_t = {}
        u_f_n_r_t['user_full_name'] = user.first_name + ' ' + user.last_name
        u_f_n_r_t['report_title'] = _report.dream_name
        user_name_report_title_list.append(u_f_n_r_t)
    ## end : for rep in repz:

    if report.type == 'group':
        print('type is group with input_count', input_count)

        group_circle_data = get_group_circle_data(connectors, input_count)

        circle_data = group_circle_data['circle_data'];
        image_name = group_circle_data['image_name'];
    ## end : if report.type == 'group':

    if report.type == 'cadence':
        cadence_circle_data = get_cadence_circle_data( \
            cadence_one_based_index, \
            connectors, \
            members)

        circle_data = cadence_circle_data['circle_data'];
        image_name = cadence_circle_data['image_name'];
    ## end : if report.type == 'cadence':

    ## Has the image been generated ?
    generate_image = True

    ## Wait up ... split the template image name into name & extension
    base_name, extension = image_name.split('.')

    ## If yes, use that instead
    base_image_partial_path = 'img/' + image_name
    # target_image_partial_url = 'tmp/' + base_name + '-' + str(id) + '.' + extension
    target_image_partial_url = 'tmp/connector-' + str(id) + '.' + extension
    ## Oddly enough, there is no elegant way of getting this freaking value
    app_name = request.path.split("/")[1]
    # print(request.path)
    # print(app_name)
    target_image_partial_path = app_name + '/static/' + target_image_partial_url
    # TODO : possible to not have to specify the app name below ?
    target_image_full_path = settings.BASE_DIR + '/' + target_image_partial_path

    # if file exists, bail generating the image
    target_image_file = Path(target_image_full_path)
    if target_image_file.exists():
        print(target_image_full_path,"already exists. not generating new image ...")
        generate_image = False

    if generate_image:
        generate_image_circle('person', circle_data, base_image_partial_path, target_image_partial_path)

    ## sharing feature
    groups = Group.objects.all()
    users = User.objects.all().exclude(is_superuser=1)

    ## get existing share records for this report
    group_shares = M_O_D_E_L_S.ReportShare.objects.filter(\
        report_stage=stage, \
        report_id=id,
        entity_type='group')
    # group_shared = 0
    if len(group_shares) > 0:
        # group_shared = 1
        for gg in groups:
            for group_share in group_shares:
                if group_share.entity_id == gg.pk:
                    gg.shared = 1

    user_shares = M_O_D_E_L_S.ReportShare.objects.filter(\
        report_stage=stage, \
        report_id=id,
        entity_type='user')
    # user_shared = 0
    if len(user_shares) > 0:
        # user_shared = 1
        for uu in users:
            for user_share in user_shares:
                if user_share.entity_id == uu.pk:
                    uu.shared = 1

    ## uri
    back_url = stage + '_index'
    pdf_url = back_url + '_pdf'

    if 'HTTP_REFERER' in request.META:
        ## Next line includes paging status :D
        back_url = request.META['HTTP_REFERER']

    page_context = {
        'circle_image_url':target_image_partial_url,
        'report':report,
        'descriptions':descriptions,
        # 'target': target,
        'target': report.type,
        'stage': stage,
        ## sharing feature
        'groups':groups,
        'users':users,
        'user_id':request.user.id,
        ## uri
        'pdf_url':pdf_url,
        'back_url':back_url,
        # next 2 are for generating the pdf
        'id': eyed,
        'app_name':app_name,
        # these are for the detail page, of course
        'user_name_report_title_list': user_name_report_title_list,
        'members': members,
    }

    generate_pdf(page_context)

    return render(request, 'connector_detail.html', page_context)

def make_array(report):
    result = []
    input_count = 12
    for x in range(1,input_count + 1):
        word_field = 'word_{0:02d}'.format(x)
        word_field_value = getattr(report, word_field)
        if word_field_value:
            v = word_field_value % input_count
            vv = 12 if v == 0 else v
            # adjust zero values
            result.append(vv)
        else:
            break

    return result

## See line 279 in www/wp-content/plugins/dreamit-connectors.php
## members should preferably be an array of id => {first_name,gender}
def get_cadence_circle_data(cadence_one_based_index, connectors, members):
    ing_cadence = konstants.ing_cadence
    patterns = konstants.connector_patterns
    # methods = konstants.connector_methods
    circle_data = {}

    for x in range(1,len(patterns)):
        archetype = patterns[x]
        for index, value in enumerate(connectors):
            # if value['arrey'][cadence_one_based_index] == x:
            if value['arrey'][cadence_one_based_index - 1] == x:
                member = next(filter(lambda m: m.id == value['user_id'], members))
                if circle_data.get(archetype):
                    circle_data[archetype].append(member.first_name)
                else:
                    circle_data[archetype] = [member.first_name]

    connectors_average = 0
    for index, value in enumerate(connectors):
        connectors_average = connectors_average + value['arrey'][cadence_one_based_index - 1]

    circle_whole_value = math.ceil(connectors_average/len(connectors))
    archetype = patterns[circle_whole_value]
    if circle_data.get(archetype):
        circle_data[archetype].append('')
    else:
        circle_data[archetype] = []

    template_image_name = (ing_cadence[cadence_one_based_index - 1]).lower() + '-connector.jpg'

    print('get_cadence_circle_data:')
    print('circle_data =',circle_data)
    print('template_image_name =',template_image_name)

    result = {
        'circle_data': circle_data,
        'image_name': template_image_name
    }

    return result

## See line 231 in www/wp-content/plugins/dreamit-connectors.php
def get_group_circle_data(connectors, input_count):
    patterns = konstants.connector_patterns
    methods = konstants.connector_methods
    circle_data = {}

    # connectors_add = []
    connectors_add = [0] * input_count
    for index, value in enumerate(connectors):
        qonnectors = []
        # for x in range(1,input_count + 1):
        for x in range(0,input_count):
            qonnectors.append(value['arrey'][x])

        for x in range(0,input_count):
            connectors_add[x] = connectors_add[x] + qonnectors[x]

    ## START : make_array
    ar = []
    for x in connectors_add:
        xx = x % 12
        xxx = 12 if xx == 0 else xx
        ar.append(xxx)
    ## END : make_array

    circle_whole_value = math.ceil(sum(ar)/input_count)

    for x in range(0,input_count):
        archetype = patterns[ar[x]]
        cadence = methods[x+1]
        if circle_data.get(archetype):
            circle_data[archetype].append(cadence)
        else:
            circle_data[archetype] = [cadence]

    archetype = patterns[circle_whole_value]
    if circle_data.get(archetype):
        circle_data[archetype].append('')
    else:
        circle_data[archetype] = []

    template_image_name = 'person-connector.jpg'

    print('get_group_circle_data:')
    print('circle_data =',circle_data)
    print('template_image_name =',template_image_name)

    result = {
        'circle_data': circle_data,
        'image_name': template_image_name
    }

    return result

## This applies to connectors of type cadence only and is used in the detail page
def copy_connector(request):
    if request.method == 'POST':
        source_id = request.POST.get('source_id')
        cadence = request.POST.get('cadence')

        print("copy connector with id ",source_id,"onto cadence",cadence)

        source = M_O_D_E_L_S.Connector.objects.get(pk=source_id)

        proceed = False

        ## Has this cadence been used ?
        if source.source is None:
            parent_pk = source_id
        else:
            parent_pk = source.source

        ## Find based on cadence & pk
        existing_1 = M_O_D_E_L_S.Connector.objects.filter(source=parent_pk,cadence=cadence)

        ## Find based on cadence & source
        existing_2 = M_O_D_E_L_S.Connector.objects.filter(pk=parent_pk,cadence=cadence)

        existing_1_2 = existing_1.union(existing_2)

        if existing_1_2.count() == 0:
            proceed = True
        else:
            source = existing_1_2.first()

        if proceed:
            # reports = source.connector_report_set.all()
            # reports = source.ConnectorReport_set.all()
            # reports = source.connectorreport_set.all()
            # reports = source.repz_set.all()
            reports = source.repz.all()

            source.pk = None
            source.cadence = cadence

            if source.source is None:
                source.source = source_id

            source.save()

            ## Copy the child records. Easier than creating an intermediary table really :P
            for report in reports:
                ## See the model definition for what 'repz' means
                source.repz.create( \
                    stage=report.stage, \
                    target=report.target, \
                    report_id=report.report_id
                )

        return redirect('connector_detail', id=source.pk)
    else:
        print("fam ... i only do POSTs")
        return HttpResponseServerError('url only supports POST')

'''
# Method to handle the 'PDF' button click
def pdf(request, id):
    return HttpResponseServerError('Not yet supported')

def pdf_email(request,id):
    return HttpResponseServerError('Not yet supported')
'''

# Method to handle the 'PDF' button click
def pdf(request, id):
    # target, stage, eyed  = request.path.split('/')[-3:]

    request_split = request.path.split('/')
    # target, stage = request_split[-4:-2]

    app_name = request_split[1]

    ## Get the full **filesystem**
    ## as the PDF generator does not handle relative web uri
    static_full_path = settings.BASE_DIR + '/' + app_name + '/static'
    pdf_full_path = static_full_path + '/tmp/connector-' + str(id) + '.pdf'

    # if file exists, return that instead
    pdf_file = Path(pdf_full_path)
    if pdf_file.exists():
        with open(pdf_full_path, 'rb') as f:
           pdf_file_data = f.read()

        return HttpResponse(pdf_file_data, content_type='application/pdf')
    else:
        return HttpResponseServerError(pdf_full_path + ' does not exists')

def pdf_email(request,id):

    has_error = False

    if request.user.is_authenticated:

        request_split = request.path.split('/')
        # target, stage = request_split[-4:-2]

        app_name = request_split[1]

        ## Get the full **filesystem**
        ## as the PDF generator does not handle relative web uri
        static_full_path = settings.BASE_DIR + '/' + app_name + '/static'
        pdf_full_path = static_full_path + '/tmp/connector-' + str(id) + '.pdf'

        # if file exists, return that instead
        pdf_file = Path(pdf_full_path)
        if pdf_file.exists():
            ## No need to do this here :)
            # with open(pdf_full_path, 'rb') as f:
               # pdf_file_data = f.read()

            report = M_O_D_E_L_S.Connector.objects.get(pk=id)

            subject = 'Your Connector ' + (report.type).capitalize() + ' report in PDF'
            message =  'Connector ' + (report.type).capitalize() + ' report and questions'
            sender = 'Human <reports@human.how>'

            try:
                email = EmailMessage()
                email.subject = subject
                email.body = message
                email.from_email = sender
                email.to = [request.user.email]
                email.attach_file(pdf_full_path)
                email.send()
            except:
                has_error = True
                ko_message = 'unable to email ' + pdf_full_path
        else:
            has_error = True
            ko_message = pdf_full_path + ' does not exists'
    else:
        has_error = True
        ko_message = 'who are you ?'
    ## end : if request.user.is_authenticated():

    if (has_error):
        return JsonResponse({'status':'ko', 'message':ko_message})
    else:
        return JsonResponse({'status':'ok'})
