import sys
import json
import random
import math

from inflector import Inflector, English
from similar_text import similar_text

from django.db.models import Q
from django.contrib.auth.models import Group, User
from django.contrib.staticfiles import finders
from django.conf import settings
from django.shortcuts import render, redirect

# Create your views here.
from django.http import JsonResponse, HttpResponse, HttpResponseServerError

# from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict
from django.template.loader import get_template
from django.core.mail.message import EmailMessage

from django.core.paginator import Paginator

# from orienters.models import SelfWord, SelfIdentifier, SelfDescriptionMale, PersonWord, PersonIdentifier, PdfPage
# from orienters.models import *
from .. import models as M_O_D_E_L_S
from .. import forms

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from .. import konstants
from .identifier import pdf, pdf_email, generate_pdf, generate_image_circle

# import render_to_pdf from utils.py
from ..utils import render_to_pdf, get_gender, get_shared_report_ids


def index(request):
    page_context = {}

    # 'identifier/self' explodes into 'identifier' & 'self'
    target, stage  = request.path.split('/')[-2:]

    form = None

    if request.method == 'POST':
        raw_words = request.POST.get('input_keywords', 'fake')
        print("Goodbye cruel world! raw_words = " + raw_words, file=sys.stderr)
        words = [int(e) if e.isdigit() else e for e in raw_words.split('|')]
        print("Hello sunshine! words = " + (' '.join(str(x) for x in words)), file=sys.stderr)
        word_ratings = [int(e) if e.isdigit() else random.randint(1,12) for e in words]

        # for word in words:
            # print('word_{0:02d}'.format(word), file=sys.stderr)

        # Use the appropriate ModelForm depending on the stage (and target)
        if stage == 'self':
            form = forms.SelfIlluminatorForm(request.POST)
        elif stage == 'voice':
            form = forms.VoiceIlluminatorForm(request.POST)
        elif stage == 'place':
            form = forms.PlaceIlluminatorForm(request.POST)
        elif stage == 'event':
            form = forms.EventIlluminatorForm(request.POST)
        elif stage == 'object':
            form = forms.ObjectIlluminatorForm(request.POST)
        elif stage == 'person':
            form = forms.PersonIlluminatorForm(request.POST)
        else:
            return HttpResponseServerError(stage + ' is not yet supported')

        print(form.errors)

        if form.is_valid():
            ## OK, but we need to do some stuff before saving ...
            # new_record = form.save()

            ## Create, but don't save the new instance
            new_record = form.save(commit=False)







            ## Modify the record in some way ...

            ## Get all illuminator words
            words = M_O_D_E_L_S.IlluminatorWord.objects.all()

            ## Get words chosen
            input_keywords = request.POST.get('input_keywords', 'fake').split('|')

            ## Init the Inflector with English
            enflector = Inflector(English)

            for index, input_keyword in enumerate(input_keywords):
                quality = 0
                for word in words:
                    ## Try original
                    if input_keyword == word.word:
                        quality = word.quality
                        break

                    ## Try singular
                    input_keyword_singular = enflector.singularize(input_keyword)
                    if input_keyword_singular == word.word:
                        quality = word.quality
                        break
                ## end : for word in words:

                if quality == 0:
                    # Try similarity
                    best_quality = 0
                    best_percent = 0
                    for word in words:
                        percent = math.floor(similar_text(word.word, input_keyword))

                        if percent > best_percent:
                            best_percent = percent
                            best_quality = word.quality

                        ## If it's rather close, stop iterating
                        if best_percent > 95:
                            break
                        ## end : if percent >= best_percent:
                    ## end : for word in words:

                    if best_percent > 80:
                        quality = best_quality
                    else:
                        quality = 7
                    ## end : if best_percent > 80:
                ## end : if quality == 0:

                word_field = 'word_{0:02d}'.format(index + 1)
                setattr(new_record, word_field, quality)

                print(str(index) + ' : ' + input_keyword + ' => ' + str(quality))
            ## end : for index, input_keyword in enumerate(input_keywords):






            ## Further record manipulation prior to saving ...

            ## Add the user id manually
            new_record.user = request.user

            ## Add the input count manually
            new_record.input_count = len(input_keywords)

            ## gender ? well, Person saves the form selection
            ## while the others use the user's gender. So ... skip ?

            ## Save the new instance
            new_record.save()

            ## Construct return (redirect ?) url
            detail_url = target + '_' + stage + '_' + 'detail'

            return redirect(detail_url, id=new_record.id)
        else:
            print('form is NOT valid. why ?')
    else:
        if stage == 'self':
            form = forms.SelfIlluminatorForm()
        elif stage == 'voice':
            form = forms.VoiceIlluminatorForm()
        elif stage == 'place':
            form = forms.PlaceIlluminatorForm()
        elif stage == 'event':
            form = forms.EventIlluminatorForm()
        elif stage == 'object':
            form = forms.ObjectIlluminatorForm()
        elif stage == 'person':
            ## The default is handled in the ModelForm class
            # form = forms.PersonIlluminatorForm(initial={'dream_gender':'male'})
            form = forms.PersonIlluminatorForm()
        else:
            return HttpResponseServerError(stage + ' is not yet supported')



    reports =  []
    user = request.user

    '''
    ## Next line returns a QuerySet object
    user_group_ids_qs = user.groups.values_list('pk',flat = True)
    ## Next line returns a list
    user_group_ids = list(user_group_ids_qs)
    print('user_group_ids:',user_group_ids)

    ## Get pk of reports shared specifically to this user and groups this user belongs to
    shared_report_ids_qs = M_O_D_E_L_S.ReportShare.objects.filter(\
        Q(report_stage=target)\
        &Q(report_target=stage)\
        &(Q(entity_type='user',entity_id=user.pk)\
        |Q(entity_type='group',entity_id__in=user_group_ids)))\
        .values_list('report_id',flat = True)\
        .distinct()

    ## Next line returns a list
    shared_report_ids = list(shared_report_ids_qs)
    print('shared_report_ids:',shared_report_ids)
    '''

    # shared_report_ids = get_shared_report_ids(stage, target, user)
    shared_report_ids = get_shared_report_ids(target, stage, user)

    # if target == 'self':
    if stage == 'self':
        ## get all order by dream_date descending
        # reports = M_O_D_E_L_S.SelfIlluminator.objects.filter(user=user).order_by('-dream_date')
        reports = M_O_D_E_L_S.SelfIlluminator.objects.filter(\
            Q(user=user)\
            |Q(pk__in=shared_report_ids))\
            .order_by('-dream_date')
    elif stage == 'voice':
        ## get all order by dream_date descending
        # reports = M_O_D_E_L_S.VoiceIlluminator.objects.filter(user=user).order_by('-dream_date')
        reports = M_O_D_E_L_S.VoiceIlluminator.objects.filter(\
            Q(user=user)\
            |Q(pk__in=shared_report_ids))\
            .order_by('-dream_date')
    elif stage == 'place':
        ## get all order by dream_date descending
        # reports = M_O_D_E_L_S.PlaceIlluminator.objects.filter(user=user).order_by('-dream_date')
        reports = M_O_D_E_L_S.PlaceIlluminator.objects.filter(\
            Q(user=user)\
            |Q(pk__in=shared_report_ids))\
            .order_by('-dream_date')
    elif stage == 'event':
        ## get all order by dream_date descending
        # reports = M_O_D_E_L_S.EventIlluminator.objects.filter(user=user).order_by('-dream_date')
        reports = M_O_D_E_L_S.EventIlluminator.objects.filter(\
            Q(user=user)\
            |Q(pk__in=shared_report_ids))\
            .order_by('-dream_date')
    elif stage == 'object':
        ## get all order by dream_date descending
        # reports = M_O_D_E_L_S.ObjectIlluminator.objects.filter(user=user).order_by('-dream_date')
        reports = M_O_D_E_L_S.ObjectIlluminator.objects.filter(\
            Q(user=user)\
            |Q(pk__in=shared_report_ids))\
            .order_by('-dream_date')
    elif stage == 'person':
        ## get all order by dream_date descending
        # reports = M_O_D_E_L_S.PersonIlluminator.objects.filter(user=user).order_by('-dream_date')
        reports = M_O_D_E_L_S.PersonIlluminator.objects.filter(\
            Q(user=user)\
            |Q(pk__in=shared_report_ids))\
            .order_by('-dream_date')
    else:
        return HttpResponseServerError(stage + ' is not yet supported')

    paginator = Paginator(reports, konstants.records_per_page) # Show 3 (?) results per page.

    page_number = request.GET.get('page', 1)
    reports_paginated = paginator.get_page(page_number)

    detail_url = target + '_' + stage + '_' + 'detail'

    page_context = {
        'reports':reports_paginated,
        'target':target,
        'stage':stage,
        'form':form,
        'input_type_choices': konstants.input_type_choices,
        'input_method_choices': konstants.input_method_choices,
        'detail_url':detail_url,
        'action':request.path
    }

    return render(request, 'illuminator.html', page_context)



def detail(request, id):
    stage, target, eyed  = request.path.split('/')[-3:]

    report = None
    patterns = None
    methods = None
    descriptions = []
    circle_data = {}


    ## Has the image been generated ?
    generate_image = True

    ## If yes, use that instead
    base_image_partial_path = 'img/' + target + "-target.jpg";
    target_image_partial_url = 'tmp/' + stage + '-' + target + '-' + str(id) + '.jpg'
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
        generate_image = False


    ## Get content for the Words section of the detail page
    if target == 'self':
        report = M_O_D_E_L_S.SelfIlluminator.objects.get(pk=id)
        patterns  = konstants.self_patterns
        methods  = konstants.self_methods
    elif target == 'voice':
        report = M_O_D_E_L_S.VoiceIlluminator.objects.get(pk=id)
        patterns  = konstants.voice_patterns
        methods  = konstants.voice_methods
    elif target == 'place':
        report = M_O_D_E_L_S.PlaceIlluminator.objects.get(pk=id)
        patterns  = konstants.place_patterns
        methods  = konstants.place_methods
    elif target == 'event':
        report = M_O_D_E_L_S.EventIlluminator.objects.get(pk=id)
        patterns  = konstants.event_patterns
        methods  = konstants.event_methods
    elif target == 'object':
        report = M_O_D_E_L_S.ObjectIlluminator.objects.get(pk=id)
        patterns  = konstants.object_patterns
        methods  = konstants.object_methods
    elif target == 'person':
        report = M_O_D_E_L_S.PersonIlluminator.objects.get(pk=id)
        patterns  = konstants.person_patterns
        methods  = konstants.person_methods
    else:
        return HttpResponseServerError(target + ' is not yet supported')


    ## Has the PDF been generated ?
    ## If yes, use that instead (Might already be the case)

    input_count = report.input_count

    for x in range(1,input_count + 1):
        word_field = 'word_{0:02d}'.format(x)
        word_field_value = getattr(report, word_field)
        archetype = patterns[word_field_value % input_count]
        cadence = methods[x]

        ## image data
        # circle_data[archetype][] = cadence
        if circle_data.get(archetype):
            circle_data[archetype].append(cadence)
        else:
            circle_data[archetype] = [cadence]

        ## Use the logged in user's gender to determine which model to use
        gender = get_gender(request)
        if target == 'self':
            if gender == 'male':
                qs = M_O_D_E_L_S.SelfDescriptionMale.objects.filter(archetype=archetype, cadence=cadence)
            else:
                qs = M_O_D_E_L_S.SelfDescriptionFemale.objects.filter(archetype=archetype, cadence=cadence)
        elif target == 'voice':
            if gender == 'male':
                qs = M_O_D_E_L_S.VoiceDescriptionMale.objects.filter(archetype=archetype, cadence=cadence)
            else:
                qs = M_O_D_E_L_S.VoiceDescriptionFemale.objects.filter(archetype=archetype, cadence=cadence)
        elif target == 'place':
            if gender == 'male':
                qs = M_O_D_E_L_S.PlaceDescriptionMale.objects.filter(archetype=archetype, cadence=cadence)
            else:
                qs = M_O_D_E_L_S.PlaceDescriptionFemale.objects.filter(archetype=archetype, cadence=cadence)
        elif target == 'event':
            if gender == 'male':
                qs = M_O_D_E_L_S.EventDescriptionMale.objects.filter(archetype=archetype, cadence=cadence)
            else:
                qs = M_O_D_E_L_S.EventDescriptionFemale.objects.filter(archetype=archetype, cadence=cadence)
        elif target == 'object':
            if gender == 'male':
                qs = M_O_D_E_L_S.ObjectDescriptionMale.objects.filter(archetype=archetype, cadence=cadence)
            else:
                qs = M_O_D_E_L_S.ObjectDescriptionFemale.objects.filter(archetype=archetype, cadence=cadence)
        elif target == 'person':
            ## Use the gender specified when making the report to determine which model to use
            if report.dream_gender == 'male':
                qs = M_O_D_E_L_S.PersonDescriptionMale.objects.filter(archetype=archetype, cadence=cadence)
            else:
                qs = M_O_D_E_L_S.PersonDescriptionFemale.objects.filter(archetype=archetype, cadence=cadence)
        else:
            return HttpResponseServerError(target + ' is not yet supported')

        ## See line 356 in ~/Documents/python_orienters/www/wp-content/plugins/dreamit-core/php/self-pfd-generator.php
        ## Use django's built in user account system
        user_name = request.user.username
        if stage != 'self':
            user_name = report.dream_name

        # descriptions.append(qs)
        for q in qs:
            # descriptions.append(q)
            q_mod = q

            report_str = q.report
            report_str_mod_1 = report_str.replace('[name]', user_name)
            report_str_mod_2 = report_str_mod_1.replace('[situation]', report.dream_name)
            q_mod.report = report_str_mod_2

            questions_str = q.questions
            questions_str_mod = questions_str.replace('[name]', user_name)
            # q_mod.questions = questions_str_mod
            ## split questions by the closing p element
            questions_split = questions_str_mod.split('</p>')
            ## remove empty entries
            questions_split_filtered = list(filter(None, questions_split))
            ## add back the end p element in each string
            [s + '</p>' for s in questions_split_filtered]
            ## set split questions back into the result object
            q_mod.questions = questions_split_filtered

            descriptions.append(q_mod)
    # END : for x in range(1,input_count + 1)

    if generate_image:
        ## What is it doing here really ?
        circle_whole_value = 0;
        # foreach ($this->patterns as $i => $arc)
        for index, value in enumerate(patterns):
            # if is_array(circle_data[value]):
            if isinstance(circle_data.get(value), (list,tuple)):
                c = len(circle_data.get(value))
                c = c if c else 0
                circle_whole_value += index * c

        circle_whole_value = round(circle_whole_value / input_count)
        archetype = patterns[circle_whole_value]
        # circle_data[archetype][] = ''
        if circle_data.get(archetype):
            circle_data[archetype].append('')
        else:
            circle_data[archetype] = []

        # base_image_partial_path = 'img/' + stage + "-target.jpg";
        # target_image_partial_url = 'tmp/' + target + '-' + stage + '-' + str(id) + '.jpg'
        ## Oddly enough, there is no elegant way of getting this freaking value
        # app_name = request.path.split("/")[1]
        # target_image_partial_path = app_name + '/static/' + target_image_partial_url
        generate_image_circle(target, circle_data, base_image_partial_path, target_image_partial_path)
    # end : if generate_image

    ## Load the image map for tooltip purposes
    map_area_file_name = target_image_full_path.replace('.jpg', '.json')
    print("map_area_file_name =",map_area_file_name)
    with open(map_area_file_name) as maf:
        map_area = json.load(maf)





    # START : answer test
    answers = M_O_D_E_L_S.ReportAnswer.objects.filter(\
        report_stage=stage, \
        report_target=target, \
        report_id=id)\
        .order_by('id','cadence','iindex')
    # END : answer test





    ## sharing feature
    groups = Group.objects.all()
    users = User.objects.all().exclude(is_superuser=1)

    ## get existing share records for this report
    group_shares = M_O_D_E_L_S.ReportShare.objects.filter(\
        report_stage=stage, \
        report_target=target, \
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
        report_target=target, \
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
    ## WARNING : this is repeated somewhere below
    back_url = stage + '_' + target
    pdf_url = back_url + '_pdf'

    if 'HTTP_REFERER' in request.META:
        ## Next line includes paging status :D
        back_url = request.META['HTTP_REFERER']

    page_context = {
        'circle_image_url':target_image_partial_url,
        'map_area':map_area,
        'report':report,
        'descriptions':descriptions,
        'answers':answers,
        'target':target,
        'stage':stage,
        ## sharing feature
        'groups':groups,
        'users':users,
        'user_id':request.user.id,
        ## uri
        'pdf_url':pdf_url,
        'back_url':back_url,
        # next 2 are for generating the pdf
        'id':id,
        'app_name':app_name,
    }

    generate_pdf(page_context)

    '''
    ## WARNING : this is already done somewhere above
    back_url = target + '_' + stage
    pdf_url = back_url + '_pdf'

    page_context = {
        'circle_image_url':'',
        'report':report,
        'descriptions':[],
        'target':target,
        'stage':stage,
        'pdf_url':pdf_url,
        'back_url':back_url,
        # next 2 are for generating the pdf
        'id':id,
        'app_name':'',
    }
    '''

    return render(request, 'illuminator_detail.html', page_context)
