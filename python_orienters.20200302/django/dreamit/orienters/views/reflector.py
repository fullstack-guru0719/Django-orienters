import sys
# from random import randrange
from pprint import pprint

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.contrib.staticfiles import finders
from django.conf import settings
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse

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

# importing get_template from loader
from django.template.loader import get_template

# import render_to_pdf from utils.py
from ..utils import render_to_pdf, get_gender, get_shared_report_ids, shared_reports_by_user, strip_tags

# from .identifier import pdf, pdf_email, generate_pdf, generate_image_circle
from .identifier import generate_pdf

@login_required
def index(request):
    stage, target  = request.path.split('/')[-2:]

    page_context = {}
    form = None

    if request.method == 'POST':

        reflector_type = request.POST.get('type', 'self|self')
        sself = request.POST.get('self')
        person1 = request.POST.get('person1')
        person2 = request.POST.get('person2')

        ## Some manual business logic intervention is needed here ...
        # if person1 != None and person2 != None:
        if isinstance(person1, list) and isinstance(person2, list):
            sself = None

        ## Create reflector record
        _c = M_O_D_E_L_S.Reflector( \
            type=reflector_type, \
            # self=self, \
            sself=sself, \
            person1=person1, \
            person2=person2, \
            # dream_space=dream_space, \
            user=request.user)
        _c.save()

        ## Construct return (redirect ?) url
        detail_url = stage + '_' + 'detail'

        return redirect(detail_url, id=_c.pk)
        # return redirect(detail_url, id=randrange(10, 99))
    else:
        users = [request.user]

        ## Get *all* reports for each user
        uzzers = []
        for user in users:
            identifier_self_reports = M_O_D_E_L_S.SelfIdentifier.objects.filter(user=user).values('id','dream_name','dream_date').order_by('-dream_date')
            for i in identifier_self_reports:
                i['stage'] = 'identifier'
                i['target'] = 'self'

            identifier_voice_reports = M_O_D_E_L_S.VoiceIdentifier.objects.filter(user=user).values('id','dream_name','dream_date').order_by('-dream_date')
            for i in identifier_voice_reports:
                i['stage'] = 'identifier'
                i['target'] = 'voice'

            identifier_place_reports = M_O_D_E_L_S.PlaceIdentifier.objects.filter(user=user).values('id','dream_name','dream_date').order_by('-dream_date')
            for i in identifier_place_reports:
                i['stage'] = 'identifier'
                i['target'] = 'place'

            identifier_event_reports = M_O_D_E_L_S.EventIdentifier.objects.filter(user=user).values('id','dream_name','dream_date').order_by('-dream_date')
            for i in identifier_event_reports:
                i['stage'] = 'identifier'
                i['target'] = 'event'

            identifier_object_reports = M_O_D_E_L_S.ObjectIdentifier.objects.filter(user=user).values('id','dream_name','dream_date').order_by('-dream_date')
            for i in identifier_object_reports:
                i['stage'] = 'identifier'
                i['target'] = 'object'

            identifier_person_reports = M_O_D_E_L_S.PersonIdentifier.objects.filter(user=user).values('id','dream_name','dream_date').order_by('-dream_date')
            for i in identifier_person_reports:
                i['stage'] = 'identifier'
                i['target'] = 'person'

            ## combine lists
            identifier_reports = list(identifier_self_reports) \
                + list(identifier_voice_reports) \
                + list(identifier_place_reports) \
                + list(identifier_event_reports) \
                + list(identifier_object_reports) \
                + list(identifier_person_reports)

            illuminator_self_reports = M_O_D_E_L_S.SelfIlluminator.objects.filter(user=user).values('id','dream_name','dream_date').order_by('-dream_date')
            for i in illuminator_self_reports:
                i['stage'] = 'illuminator'
                i['target'] = 'self'

            illuminator_voice_reports = M_O_D_E_L_S.VoiceIlluminator.objects.filter(user=user).values('id','dream_name','dream_date').order_by('-dream_date')
            for i in illuminator_voice_reports:
                i['stage'] = 'illuminator'
                i['target'] = 'voice'

            illuminator_place_reports = M_O_D_E_L_S.PlaceIlluminator.objects.filter(user=user).values('id','dream_name','dream_date').order_by('-dream_date')
            for i in illuminator_place_reports:
                i['stage'] = 'illuminator'
                i['target'] = 'place'

            illuminator_event_reports = M_O_D_E_L_S.EventIlluminator.objects.filter(user=user).values('id','dream_name','dream_date').order_by('-dream_date')
            for i in illuminator_event_reports:
                i['stage'] = 'illuminator'
                i['target'] = 'event'

            illuminator_object_reports = M_O_D_E_L_S.ObjectIlluminator.objects.filter(user=user).values('id','dream_name','dream_date').order_by('-dream_date')
            for i in illuminator_object_reports:
                i['stage'] = 'illuminator'
                i['target'] = 'object'

            illuminator_person_reports = M_O_D_E_L_S.PersonIlluminator.objects.filter(user=user).values('id','dream_name','dream_date').order_by('-dream_date')
            for i in illuminator_person_reports:
                i['stage'] = 'illuminator'
                i['target'] = 'person'

            ## combine lists
            illuminator_reports = list(illuminator_self_reports) \
                + list(illuminator_voice_reports) \
                + list(illuminator_place_reports) \
                + list(illuminator_event_reports) \
                + list(illuminator_object_reports) \
                + list(illuminator_person_reports)

            ## combine lists
            reports = identifier_reports + illuminator_reports

            ## To sort the list in place...
            # reports.sort(key=lambda x: x.dream_date, reverse=True)
            reports.sort(key=lambda x: x['dream_date'], reverse=True)

            ## construct our custom dict (?)
            uzzer = {
                'id' : user.id,
                'first_name' : user.first_name,
                'last_name' : user.last_name,
                'username' : user.username,
                'reports' : reports,
                'report_count' : len(reports)}
                # 'identifier_reports' : identifier_reports,
                # 'illuminator_reports' : illuminator_reports,
                # 'report_count' : len(identifier_reports) + len(illuminator_reports)}

            uzzers.append(uzzer)
            # uzzers.extend(uzzer)
        ## end : for user in users

        ## Get list of users in the user's group, excluding the user themself
        first_group = user.groups.first()
        group_members = first_group.user_set.all().exclude(pk=user.pk).only('id','first_name','last_name','username')
        # print(group_members)

        shared_report_ids = get_shared_report_ids('reflector', None, user)

        ## START : get reflectors by dream_date descending
        # reports = M_O_D_E_L_S.Reflector.objects.all().order_by('-dream_date')
        reports = M_O_D_E_L_S.Reflector.objects.filter(\
            Q(user=user)\
            |Q(pk__in=shared_report_ids))\
            .order_by('-dream_date')
        paginator = Paginator(reports, konstants.records_per_page) # Show konstants.records_per_page results per page.

        page_number = request.GET.get('page', 1)
        reports_paginated = paginator.get_page(page_number)

        # reports = M_O_D_E_L_S.Reflector.objects.all().order_by('-dream_date')

        ## get report1 and report2 manually for each report
        for report in reports_paginated:
            report_self = None
            report_person1 = None
            report_person2 = None

            if report.sself:
                stage,target,report_id = (report.sself).split("|")
                result = get_report(stage,target,report_id)
                # report_self = result.report
                report_self = result['report']

            if report.person1:
                stage,target,report_id = (report.person1).split("|")
                result = get_report(stage,target,report_id)
                # report_person1 = result.report
                report_person1 = result['report']

            if report.person2:
                stage,target,report_id = (report.person2).split("|")
                result = get_report(stage,target,report_id)
                # report_person2 = result.report
                report_person2 = result['report']

            if report.type == 'self|self':
                report.derived_name = report_self.dream_name
            elif report.type == 'self|person':
                report.derived_name = report_self.dream_name + " vs " + report_person2.dream_name
            elif report.type == 'person|self':
                report.derived_name = report_person1.dream_name + " vs " + report_self.dream_name
            # if report.type == 'person|person':
            else:
                report.derived_name = report_person1.dream_name + " vs " + report_person2.dream_name

        ## end : for report in reports
        ## END : get reflectors by dream_date descending

        page_context = {
            'uzzers' : uzzers,
            'group_members' : group_members,
            'reports' : reports_paginated}

    return render(request, 'reflector.html', page_context)

def reports_by_user(request, user_id):
    user = User.objects.get(pk=user_id)
    result = shared_reports_by_user(request, user)

    ## combine lists
    reports = result['identifier_reports'] + result['illuminator_reports']

    ## To sort the list in place...
    reports.sort(key=lambda x: x['dream_date'], reverse=True)

    ## construct our custom dict (?)
    uzzer = {
        'id' : user.id,
        'first_name' : user.first_name,
        'last_name' : user.last_name,
        'username' : user.username,
        'reports' : reports,
        'report_count' : len(reports)}

    data = {
        'user': uzzer
    }
    return JsonResponse(data)

@login_required
def detail(request, id):
    # target, eyed = request.path.split('/')[-2:]
    app_name, stage, eyed = request.path.split('/')[-3:]

    print('~~~~~~ id = ' + eyed)

    ## Use the logged in user's gender to determine which model to use
    # gender = get_gender(request)

    ## START : the nitty gritty
    page_context = {}
    template = None

    report = M_O_D_E_L_S.Reflector.objects.get(pk=id)
    _type = report.type

    report1 = None
    patterns1 = None
    # methods1 = None
    stage1 = None
    target1 = None
    array1 = None

    report2 = None
    patterns2 = None
    # methods2 = None
    stage2 = None
    target2 = None
    array2 = None

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

    ## Part 1

    ## The following doesn't look Pythonic :/
    if _type == 'self|self':
        result1 = get_self_report(report)
        report1 = result1['report']
        patterns1 = result1['patterns']
        # methods1 = result1['methods']
        stage1 = result1['stage']
        target1 = result1['target']

    if _type == 'self|person':
        result1 = get_self_report(report)
        report1 = result1['report']
        patterns1 = result1['patterns']
        # methods1 = result1['methods']
        stage1 = result1['stage']
        target1 = result1['target']

        result2 = get_person2_report(report)
        report2 = result2['report']
        patterns2 = result2['patterns']
        # methods2 = result2['methods']
        stage2 = result2['stage']
        target2 = result2['target']

    if _type == 'person|self':
        result1 = get_person1_report(report)
        report1 = result1['report']
        patterns1 = result1['patterns']
        # methods1 = result1['methods']
        stage1 = result1['stage']
        target1 = result1['target']

        result2 = get_self_report(report)
        report2 = result2['report']
        patterns2 = result2['patterns']
        # methods2 = result2['methods']
        stage2 = result2['stage']
        target2 = result2['target']

    if _type == 'person|person':
        result1 = get_person1_report(report)
        report1 = result1['report']
        patterns1 = result1['patterns']
        # methods1 = result1['methods']
        stage1 = result1['stage']
        target1 = result1['target']

        result2 = get_person2_report(report)
        report2 = result2['report']
        patterns2 = result2['patterns']
        # methods2 = result2['methods']
        stage2 = result2['stage']
        target2 = result2['target']

    array1 = make_array(report1)

    print("array1 =",array1)

    if report2:
        array2 = make_array(report2)

        print("array2 =",array2)


    print("_type =",_type)

    ## Part 2
    if _type == 'self|self':
        gender = get_gender_from_report(report1)

        c = len(array1)

        # ea_right = []
        # ea_left = []

        ea_right = [None] * c
        ea_left = [None] * c

        # for idx in range(1,c):
        # for idx in range(1,c+1):
        for idx in range(c):
            # j = 1
            # foreach ($this->patterns as $i => $arc)
            j_array = []

            for index, value in enumerate(array1):
                j_array.append([index,value])

            ea_right[idx] = j_array

        print("ea_right =")
        pprint(ea_right)

        for index, value in enumerate(ea_right):
            # if index == 0:
                # continue

            j_array = []

            # for j in range(1,c):
            # for j in range(1,c+1):
            for j in range(c):
                # j_array.append([value[index][1], value[index][2]])
                j_array.append([value[index][0], value[index][1]])
                # j_array.append([value[j][0], value[j][1]])

            ea_left[index] = j_array

        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("ea_left =")
        pprint(ea_left)

        # aas = []
        # aspect_descriptions = []
        # archetype_images = []

        aas = [None] * c
        aspect_descriptions = [None] * c
        archetype_images = [None] * c

        # i = 1
        i = 0
        # for index, value in enumerate(array1):
        for value in array1:
            # j = 1
            j = 0
            archetype_images[i] = (patterns1[value]).lower() + "50.gif"

            _desc = []

            # j_array = []
            j_array = [None] * c

            # for index2, value2 in enumerate(array1):
            for value2 in array1:
                if value2 - value < 0:
                    j_array[j] = 12 - (12 + value2 - value) + 1
                else:
                    j_array[j] = 12 - (value2 - value) + 1

                aas[i] = j_array

                row2use = 1 if value2 == 13 else value2
                cadence = i + 1
                asuse = 1 if aas[i][j] == 13 else aas[i][j]

                ## assign aspect to cadence arquetype first: $eaLeft < ---
                ## (huh ?)
                # ea_left[j][i][3] = asuse
                ea_left[j][i].append(asuse)
                ## this number is relevating, must be 1!
                ## (huh ?)
                # ea_right[i][j][3] = 1
                ea_right[i][j].append(1)

                '''
                print("----------------")
                print("i j = " + str(i) + " " + str(j))
                print("aas = ",aas)
                print("row2use = archetype =",row2use)
                print("cadence =",cadence)
                print("asuse = aspect = ",asuse)
                print("ea_left[j] = ",ea_left[j])
                print("ea_left[j][i] = ",ea_left[j][i])
                '''

                if gender == "male":
                    qs = M_O_D_E_L_S.SelfSelfAspectDescriptionMale.objects.filter(archetype=row2use, cadence=cadence, aspect=asuse)
                else:
                    qs = M_O_D_E_L_S.SelfSelfAspectDescriptionFemale.objects.filter(archetype=row2use, cadence=cadence, aspect=asuse)

                q = qs[0]
                _desc.append(q);

                j = j + 1

            aspect_descriptions[i] = _desc
            i = i + 1

        '''
        print("len(aspect_descriptions) =",len(aspect_descriptions))
        print("archetype_images =",archetype_images)
        print("----------------")
        '''

        ## get words of cadence arquetype first
        # words_left = []
        words_left = [None] * c
        for index, value in enumerate(ea_left):

            # print("left : value = ",value)
            print("left : index =",index)
            print("value =")
            pprint(value)

            for j, tern in enumerate(value):

                # print("left : tern = ",tern)

                if gender == "male":
                    qs = M_O_D_E_L_S.SelfSelfAspectDescriptionMale.objects.filter(archetype=tern[1], cadence=tern[0] + 1, aspect=tern[2])
                else:
                    qs = M_O_D_E_L_S.SelfSelfAspectDescriptionFemale.objects.filter(archetype=tern[1], cadence=tern[0] + 1, aspect=tern[2])
                ## end : if gender == "male":

                q = qs[0]

                ## Modify some properties
                text_1_mod = strip_tags(q.text_1)
                q.text_1 = text_1_mod

                ## PHP : $wordsLeft[$i][$j] = $wpdb->get_row($sql);
                if words_left[index]:
                    words_left[index][j] = q
                else:
                    # _tmp_array = []
                    _tmp_array = [None] * len(value)
                    _tmp_array[j] = q
                    words_left[index] = _tmp_array
                ## end : if words_left.get(j):

        ## get words of cadence arquetype second
        # words_right = []
        words_right = [None] * c
        for index, value in enumerate(ea_right):

            # print("right : value = ",value)
            print("right : index =",index)
            print("value =")
            pprint(value)

            for j, tern in enumerate(value):

                # print("right : tern = ",tern)

                if gender == "male":
                    qs = M_O_D_E_L_S.SelfSelfAspectDescriptionMale.objects.filter(archetype=tern[1], cadence=tern[0] + 1, aspect=tern[2])
                else:
                    qs = M_O_D_E_L_S.SelfSelfAspectDescriptionFemale.objects.filter(archetype=tern[1], cadence=tern[0] + 1, aspect=tern[2])
                ## end : if gender == "male":

                q = qs[0]

                ## Modify some properties
                text_6_mod = strip_tags(q.text_6)
                q.text_6 = text_6_mod

                ## PHP : $$wordsRight[$i][$j] = $wpdb->get_row($sql);
                if words_right[index]:
                    words_right[index][j] = q
                else:
                    # _tmp_array = []
                    _tmp_array = [None] * len(value)
                    _tmp_array[j] = q
                    words_right[index] = _tmp_array
                ## end : if words_right.get(j):

        lc_ing_cadence = [x.lower() for x in konstants.ing_cadence]

        ## Non-helpful debugging ...
        # print("words_left =",words_left)
        # print("words_right =",words_right)
        # print("lc_ing_cadence =",lc_ing_cadence)

        ## uri
        # back_url = stage + '_index'
        # back_url = reverse('reflector.index')
        back_url = reverse('reflector_index')

        if 'HTTP_REFERER' in request.META:
            ## Next line includes paging status :D
            back_url = request.META['HTTP_REFERER']

        page_context = {
            'circle_image_url':'',
            'report':report,
            'report1':report1,
            'words_right':words_right,
            'words_left':words_left,
            'aspect_descriptions':aspect_descriptions,
            'archetype_images':archetype_images,
            'ing_cadence':lc_ing_cadence,
            ## sharing feature
            'groups':groups,
            'users':users,
            'user_id':request.user.id,
            'pdf_url':'',
            # 'back_url': 'reflector_index',
            # 'back_url':request.get_full_path,
            'back_url':back_url,
            # the folowing are for generating the pdf
            'id': eyed,
            'app_name':app_name,
            'stage':stage,
            'target':_type,
            'descriptions':[]
        }

        template = 'reflector_detail.html'
    ## end : if _type == 'self|self':

    ## +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    ## -----------------------------------------------------
    ## -----------------------------------------------------
    ## -----------------------------------------------------
    ## -----------------------------------------------------
    ## -----------------------------------------------------
    ## -----------------------------------------------------
    ## +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

    if (_type == 'self|person') or (_type == 'person|self') or (_type == 'person|person'):
        first_name1 = report1.user.first_name
        first_name2 = report2.user.first_name

        gender1 = "male"
        gender2 = "male"

        gender1 = get_gender_from_report(report1)
        gender2 = get_gender_from_report(report2)

        if _type == 'self|person':
            gender = gender2

        if _type == 'person|self':
            gender = gender1

        if _type == 'person|person':
            gender = gender2

        '''
        ## done earlier
        array1 = make_array(report1)
        if report2:
            array2 = make_array(report2)
        '''

        kount1 = len(array1)
        kount2 = len(array2)
        c = kount1

        ## adjust both arrays length
        if (stage1 == 'illuminator' or stage2 == 'illuminator'):
            if (kount1 < kount2):
                array2 = array2[:kount1]
            if (kount2 < kount1):
                array1 = array1[:kount2]
            c = min(kount1, kount2)
        ## end : if (stage1 == 'illuminator' or stage2 == 'illuminator'):

        print("c = ",c)
        print("trimmed array1 = ",array1)
        print("trimmed array2 = ",array2)

        # ea_right = []
        # ea_left = []

        # ea_right = [None] * kount2
        # ea_left = [None] * kount1

        ea_right = [None] * c
        ea_left = [None] * c

        # for idx in range(1,kount2):
        # for idx in range(1,kount2+1):
        # for idx in range(kount2):
        for idx in range(c):
            # j = 1
            # foreach ($this->patterns as $i => $arc)
            j_array = []

            for index, value in enumerate(array2):
                j_array.append([index,value])

            ea_right[idx] = j_array

        print("ea_right =")
        pprint(ea_right)


        # for idx in range(1,kount1):
        # for idx in range(1,kount1+1):
        # for idx in range(kount1):
        for idx in range(c):
            # j = 1
            # foreach ($this->patterns as $i => $arc)
            j_array = []

            for index, value in enumerate(array1):
                j_array.append([index,value])

            ea_left[idx] = j_array

        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("ea_left =")
        pprint(ea_left)


        ## The f*** is this ? See line 444 in /home/pmg/Documents/python_orienters/www/wp-content/plugins/dreamit-reflectors.php

        # archetype_images1 = [None] * kount1
        # archetype_images2 = [None] * kount2

        archetype_images1 = [None] * c
        archetype_images2 = [None] * c

        for index, value in enumerate(array1):
            '''
            if _type == "self|person":
                archetype_images1[index] = (patterns1[value]).lower() + "50.gif"

            if (_type == "person|self") or (_type == "person|person"):
                archetype_images1[index] = (patterns1[value]).lower() + "50.gif"
            '''
            archetype_images1[index] = (patterns1[value]).lower() + "50.gif"

        for index, value in enumerate(array2):
            '''
            if (_type == "self|person") or (_type == "person|person"):
                archetype_images2[index] = (patterns2[value]).lower() + "50.gif"

            if _type == "person|self":
                archetype_images2[index] = (patterns2[value]).lower() + "50.gif"
            '''
            archetype_images2[index] = (patterns2[value]).lower() + "50.gif"

        # aas = []
        # aspect_descriptions = []

        # aas = [None] * c
        # aspect_descriptions = [None] * c

        aas = [None] * kount2
        aspect_descriptions = [None] * kount2

        # i = 1
        i = 0
        # for index, value in enumerate(array2):
        for value in array2:
            # j = 1
            j = 0

            _desc = []

            # j_array = []
            # j_array = [None] * c
            # j_array = [None] * kount2
            j_array = [None] * kount1

            # for index2, value2 in enumerate(array1):
            for value2 in array1:
                if value2 - value < 0:
                    j_array[j] = 12 - (12 + value2 - value) + 1
                else:
                    j_array[j] = 12 - (value2 - value) + 1

                aas[i] = j_array

                row2use = 1 if value2 == 13 else value2
                cadence = i + 1
                asuse = 1 if aas[i][j] == 13 else aas[i][j]

                ## assign aspect to cadence arquetype first: $eaLeft < ---
                ## (huh ?)
                # ea_left[i][j][3] = asuse
                ea_left[i][j].append(asuse)
                ## this number is relevating, must be 1!
                ## (huh ?)
                # ea_right[j][i][3] = 1
                ea_right[j][i].append(1)

                '''
                print("----------------")
                print("i j = " + str(i) + " " + str(j))
                print("aas = ",aas)
                print("row2use = archetype =",row2use)
                print("cadence =",cadence)
                print("asuse = aspect = ",asuse)
                print("ea_left[i] = ",ea_left[i])
                print("ea_left[i][j] = ",ea_left[i][j])
                print("ea_right[j] = ",ea_right[j])
                print("ea_right[j][i] = ",ea_right[j][i])
                '''

                if gender == "male":
                    if _type == 'self|person':
                        qs = M_O_D_E_L_S.SelfPersonAspectDescriptionMale.objects.filter(archetype=row2use, cadence=cadence, aspect=asuse)
                    elif _type == 'person|self':
                        qs = M_O_D_E_L_S.PersonSelfAspectDescriptionMale.objects.filter(archetype=row2use, cadence=cadence, aspect=asuse)
                    # elif _type == 'person|person':
                    else:
                        qs = M_O_D_E_L_S.PersonPersonAspectDescriptionMale.objects.filter(archetype=row2use, cadence=cadence, aspect=asuse)
                else:
                    if _type == 'self|person':
                        qs = M_O_D_E_L_S.SelfPersonAspectDescriptionFemale.objects.filter(archetype=row2use, cadence=cadence, aspect=asuse)
                    elif _type == 'person|self':
                        qs = M_O_D_E_L_S.PersonSelfAspectDescriptionFemale.objects.filter(archetype=row2use, cadence=cadence, aspect=asuse)
                    # elif _type == 'person|person':
                    else:
                        qs = M_O_D_E_L_S.PersonPersonAspectDescriptionFemale.objects.filter(archetype=row2use, cadence=cadence, aspect=asuse)

                q = qs[0]
                _desc.append(q);

                j = j + 1

            aspect_descriptions[i] = _desc
            i = i + 1

        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("len(aspect_descriptions) =",len(aspect_descriptions))
        # print("archetype_images1 =")
        # pprint(archetype_images1)
        # print("archetype_images2 =")
        # pprint(archetype_images2)

        ## get words of cadence arquetype first
        # words_left = []
        words_left = [None] * c
        # words_left = [None] * kount2
        for index, value in enumerate(ea_left):

            # print("left : index value = ",index,value)

            for j, tern in enumerate(value):

                # print("left : j tern = ",j,tern)

                if gender1 == "male":
                    if _type == 'self|person':
                        qs = M_O_D_E_L_S.SelfPersonAspectDescriptionMale.objects.filter(archetype=tern[1], cadence=tern[0] + 1, aspect=tern[2])
                    elif _type == 'person|self':
                        qs = M_O_D_E_L_S.PersonSelfAspectDescriptionMale.objects.filter(archetype=tern[1], cadence=tern[0] + 1, aspect=tern[2])
                    # elif _type == 'person|person':
                    else:
                        qs = M_O_D_E_L_S.PersonPersonAspectDescriptionMale.objects.filter(archetype=tern[1], cadence=tern[0] + 1, aspect=tern[2])
                else:
                    if _type == 'self|person':
                        qs = M_O_D_E_L_S.SelfPersonAspectDescriptionFemale.objects.filter(archetype=tern[1], cadence=tern[0] + 1, aspect=tern[2])
                    elif _type == 'person|self':
                        qs = M_O_D_E_L_S.PersonSelfAspectDescriptionFemale.objects.filter(archetype=tern[1], cadence=tern[0] + 1, aspect=tern[2])
                    # elif _type == 'person|person':
                    else:
                        qs = M_O_D_E_L_S.PersonPersonAspectDescriptionFemale.objects.filter(archetype=tern[1], cadence=tern[0] + 1, aspect=tern[2])
                ## end : if gender == "male":

                q = qs[0]

                ## Modify some properties
                text_1_mod = strip_tags(q.text_1)
                q.text_1 = text_1_mod

                if _type == 'self|person':
                    text_1_str = q.text_1
                    q.text_1 = text_1_str.replace('[name2]', first_name2)

                    text_3_str = q.text_3
                    q.text_3 = text_3_str.replace('[name2]', first_name2)

                    text_5_str = q.text_5
                    q.text_5 = text_5_str.replace('[name2]', first_name2)
                elif _type == 'person|self':
                    text_1_str = q.text_1
                    q.text_1 = text_1_str.replace('[name1]', first_name2)

                    text_3_str = q.text_3
                    q.text_3 = text_3_str.replace('[name1]', first_name2)

                    text_5_str = q.text_5
                    q.text_5 = text_5_str.replace('[name1]', first_name2)
                # elif _type == 'person|person':
                else:
                    text_1_str = q.text_1
                    text_1_str_mod = text_1_str.replace('[name1]', first_name1)
                    q.text_1 = text_1_str_mod.replace('[name2]', first_name2)

                    text_3_str = q.text_3
                    text_3_str_mod = text_3_str.replace('[name1]', first_name1)
                    q.text_3 = text_3_str_mod.replace('[name2]', first_name2)

                    text_5_str = q.text_5
                    text_5_str_mod = text_5_str.replace('[name1]', first_name1)
                    q.text_5 = text_5_str_mod.replace('[name2]', first_name2)

                ## PHP : $wordsLeft[$j][$i] = $wpdb->get_row($sql);
                if words_left[j]:
                    # words_left[j].append(q)
                    words_left[j][index] = q
                else:
                    # _tmp_array = []
                    _tmp_array = [None] * len(value)
                    _tmp_array[index] = q
                    words_left[j] = _tmp_array
                ## end : if words_left.get(j):
            ## end : for j, tern in enumerate(value):
        ## end : for index, value in enumerate(ea_left):

        ## get words of cadence arquetype second
        # words_right = []
        words_right = [None] * c
        for index, value in enumerate(ea_right):

            # print("right : index value = ",index,value)

            for j, tern in enumerate(value):

                # print("right : j tern = ",j,tern)

                if gender == "male":
                    if _type == 'self|person':
                        qs = M_O_D_E_L_S.SelfPersonAspectDescriptionMale.objects.filter(archetype=tern[1], cadence=tern[0] + 1, aspect=tern[2])
                    elif _type == 'person|self':
                        qs = M_O_D_E_L_S.PersonSelfAspectDescriptionMale.objects.filter(archetype=tern[1], cadence=tern[0] + 1, aspect=tern[2])
                    # elif _type == 'person|person':
                    else:
                        qs = M_O_D_E_L_S.PersonPersonAspectDescriptionMale.objects.filter(archetype=tern[1], cadence=tern[0] + 1, aspect=tern[2])
                else:
                    if _type == 'self|person':
                        qs = M_O_D_E_L_S.SelfPersonAspectDescriptionFemale.objects.filter(archetype=tern[1], cadence=tern[0] + 1, aspect=tern[2])
                    elif _type == 'person|self':
                        qs = M_O_D_E_L_S.PersonSelfAspectDescriptionFemale.objects.filter(archetype=tern[1], cadence=tern[0] + 1, aspect=tern[2])
                    # elif _type == 'person|person':
                    else:
                        qs = M_O_D_E_L_S.PersonPersonAspectDescriptionFemale.objects.filter(archetype=tern[1], cadence=tern[0] + 1, aspect=tern[2])
                ## end : if gender == "male":

                q = qs[0]

                ## Modify some properties
                text_6_mod = strip_tags(q.text_6)
                q.text_6 = text_6_mod

                if _type == 'self|person':
                    text_2_str = q.text_2
                    q.text_2 = text_2_str.replace('[name2]', first_name2)

                    text_4_str = q.text_4
                    q.text_4 = text_4_str.replace('[name2]', first_name2)

                    text_6_str = q.text_6
                    q.text_6 = text_6_str.replace('[name2]', first_name2)
                elif _type == 'person|self':
                    text_2_str = q.text_2
                    q.text_2 = text_2_str.replace('[name1]', first_name1)

                    text_4_str = q.text_4
                    q.text_4 = text_4_str.replace('[name1]', first_name1)

                    text_6_str = q.text_6
                    q.text_6 = text_6_str.replace('[name1]', first_name1)
                # elif _type == 'person|person':
                else:
                    text_2_str = q.text_2
                    text_2_str_mod = text_2_str.replace('[name1]', first_name1)
                    q.text_2 = text_2_str_mod.replace('[name2]', first_name2)

                    text_4_str = q.text_4
                    text_4_str_mod = text_4_str.replace('[name1]', first_name1)
                    q.text_4 = text_4_str_mod.replace('[name2]', first_name2)

                    text_6_str = q.text_6
                    text_6_str_mod = text_6_str.replace('[name1]', first_name1)
                    q.text_6 = text_6_str_mod.replace('[name2]', first_name2)

                ## PHP : $wordsRight[$i][$j] = $wpdb->get_row($sql);
                if words_right[index]:
                    words_right[index][j] = q
                else:
                    # _tmp_array = []
                    _tmp_array = [None] * len(value)
                    _tmp_array[j] = q
                    words_right[index] = _tmp_array
                ## end : if words_right.get(index):
            ## end : for j, tern in enumerate(value):
        ## end : for index, value in enumerate(ea_right):

        lc_ing_cadence = [x.lower() for x in konstants.ing_cadence[:c]]

        print("lc_ing_cadence =")
        pprint(lc_ing_cadence)

        ## uri
        # back_url = stage + '_index'
        # back_url = reverse('reflector.index')
        back_url = reverse('reflector_index')

        if 'HTTP_REFERER' in request.META:
            ## Next line includes paging status :D
            back_url = request.META['HTTP_REFERER']

        page_context = {
            'type':_type,
            'report':report,
            'report1':report1,
            'report2':report2,
            'first_name1':first_name1,
            'first_name2':first_name2,
            'words_left':words_left,
            'words_right':words_right,
            'aspect_descriptions':aspect_descriptions,
            'archetype_images1':archetype_images1,
            'archetype_images2':archetype_images2,
            'ing_cadence':lc_ing_cadence,
            ## sharing feature
            'groups':groups,
            'users':users,
            'user_id':request.user.id,
            'pdf_url':'',
            # 'back_url': 'reflector_index',
            # 'back_url':request.get_full_path,
            'back_url':back_url,
            # the folowing are for generating the pdf
            'id': eyed,
            'app_name':app_name,
            'stage':stage,
            ## Don't do this here as it will break ORM queries in generate_pdf
            # 'target':_"-".join(x.capitalize() for x in target.split("|"))
            'target':_type,
            'descriptions':[]
        }

        template = 'reflector_detail_2.html'

    ## end : if (_type == 'self|person') or (_type == 'person|self') or (_type == 'person|person'):

    ## END : the nitty gritty

    generate_pdf(page_context)

    return render(request, template, page_context)

def get_self_report(report):
    stage,target,id = report.sself.split("|")
    return get_report(stage,target,id)

def get_person1_report(report):
    stage,target,id = report.person1.split("|")
    return get_report(stage,target,id)

def get_person2_report(report):
    stage,target,id = report.person2.split("|")
    return get_report(stage,target,id)

def get_report(stage,target,id):
    if stage == "identifier":
        if target == 'self':
            report = M_O_D_E_L_S.SelfIdentifier.objects.get(pk=id)
            patterns = konstants.self_patterns
            # methods = konstants.self_methods
        elif target == 'voice':
            report = M_O_D_E_L_S.VoiceIdentifier.objects.get(pk=id)
            patterns = konstants.voice_patterns
            # methods = konstants.voice_methods
        elif target == 'place':
            report = M_O_D_E_L_S.PlaceIdentifier.objects.get(pk=id)
            patterns = konstants.place_patterns
            # methods = konstants.place_methods
        elif target == 'event':
            report = M_O_D_E_L_S.EventIdentifier.objects.get(pk=id)
            patterns = konstants.event_patterns
            # methods = konstants.event_methods
        elif target == 'object':
            report = M_O_D_E_L_S.ObjectIdentifier.objects.get(pk=id)
            patterns = konstants.object_patterns
            # methods = konstants.object_methods
        elif target == 'person':
            report = M_O_D_E_L_S.PersonIdentifier.objects.get(pk=id)
            patterns = konstants.person_patterns
            # methods = konstants.person_methods
        else:
            return HttpResponseServerError(target + ' is not yet supported')


    if stage == "illuminator":
        if target == 'self':
            report = M_O_D_E_L_S.SelfIlluminator.objects.get(pk=id)
            patterns = konstants.self_patterns
            # methods = konstants.self_methods
        elif target == 'voice':
            report = M_O_D_E_L_S.VoiceIlluminator.objects.get(pk=id)
            patterns = konstants.voice_patterns
            # methods = konstants.voice_methods
        elif target == 'place':
            report = M_O_D_E_L_S.PlaceIlluminator.objects.get(pk=id)
            patterns = konstants.place_patterns
            # methods = konstants.place_methods
        elif target == 'event':
            report = M_O_D_E_L_S.EventIlluminator.objects.get(pk=id)
            patterns = konstants.event_patterns
            # methods = konstants.event_methods
        elif target == 'object':
            report = M_O_D_E_L_S.ObjectIlluminator.objects.get(pk=id)
            patterns = konstants.object_patterns
            # methods = konstants.object_methods
        elif target == 'person':
            report = M_O_D_E_L_S.PersonIlluminator.objects.get(pk=id)
            patterns = konstants.person_patterns
            # methods = konstants.person_methods
        else:
            return HttpResponseServerError(target + ' is not yet supported')

    # return report
    return {
        'report': report,
        'patterns': patterns,
        # 'methods': methods,
        'stage': stage,
        'target': target}

def get_gender_from_report(report):
    user = report.user

    gender = "male"
    if hasattr(user, 'human'):
        gender = user.human.gender

    ## if report has dream_gender, use that instead
    if hasattr(report, 'dream_gender'):
        gender = report.dream_gender

    return gender

def make_array(report):
    input_count = 12

    _input_count = getattr(report, 'input_count', input_count)
    if _input_count:
        input_count = _input_count

    rs = []

    for x in range(1,input_count + 1):
        word_field = 'word_{0:02d}'.format(x)
        word_field_value = getattr(report, word_field)
        # archetype = patterns[word_field_value % input_count]
        # cadence = methods[x]
        ## This means rs is a zero indexed array
        rs.append(word_field_value % input_count)

    ## Adjusts 0 to 12
    result = [12 if int(r)==0 else r for r in rs]

    return result

# Method to handle the 'PDF' button click
def pdf(request, id):
    # target, stage, eyed  = request.path.split('/')[-3:]

    request_split = request.path.split('/')
    # target, stage = request_split[-4:-2]

    app_name = request_split[1]

    ## Get the full **filesystem**
    ## as the PDF generator does not handle relative web uri
    static_full_path = settings.BASE_DIR + '/' + app_name + '/static'
    pdf_full_path = static_full_path + '/tmp/reflector-' + str(id) + '.pdf'

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
        pdf_full_path = static_full_path + '/tmp/reflector-' + str(id) + '.pdf'

        # if file exists, return that instead
        pdf_file = Path(pdf_full_path)
        if pdf_file.exists():
            ## No need to do this here :)
            # with open(pdf_full_path, 'rb') as f:
               # pdf_file_data = f.read()

            report = M_O_D_E_L_S.Connector.objects.get(pk=id)

            subject = 'Your Reflector ' + (report.type).capitalize() + ' report in PDF'
            message =  'Reflector ' + (report.type).capitalize() + ' report'
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
