import sys
import json

from django.contrib.auth.models import Group, User
from django.contrib.staticfiles import finders
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
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

# from bs4 import BeautifulSoup

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from pprint import pprint
from .. import konstants

# import render_to_pdf from utils.py
from ..utils import render_to_pdf, get_gender, get_shared_report_ids


def self_words(request):
    # get all but in random order
    words = M_O_D_E_L_S.SelfWord.objects.all().order_by('?')
    return render(request, 'shared/words.html', {'words':words})

def index(request):
    ## 'identifier/self' explodes into 'identifier' & 'self'
    ## Next line should started with 'stage, target'. Still works as is though :)
    target, stage  = request.path.split('/')[-2:]

    form = None

    if request.method == 'POST':

        raw_words = request.POST.get('words', 'fake')
        print("Goodbye cruel world! raw_words = " + raw_words, file=sys.stderr)
        words = [int(e) if e.isdigit() else e for e in raw_words.split(',')]
        print("Hello sunshine! words = " + (' '.join(str(x) for x in words)), file=sys.stderr)

        # for word in words:
            # print('word_{0:02d}'.format(word), file=sys.stderr)

        # Use the appropriate ModelForm depending on the stage (and target)
        if stage == 'self':
            form = forms.SelfIdentifierForm(request.POST)
        elif stage == 'voice':
            form = forms.VoiceIdentifierForm(request.POST)
        elif stage == 'place':
            form = forms.PlaceIdentifierForm(request.POST)
        elif stage == 'event':
            form = forms.EventIdentifierForm(request.POST)
        elif stage == 'object':
            form = forms.ObjectIdentifierForm(request.POST)
        elif stage == 'person':
            form = forms.PersonIdentifierForm(request.POST)
        else:
            return HttpResponseServerError(stage + ' is not yet supported')

        if form.is_valid():
            ## OK, but we need to do some stuff before saving ...
            # new_record = form.save()

            ## Create, but don't save the new instance
            new_record = form.save(commit=False)

            ## Modify the record in some way ...

            ## The following looks hella lame
            # new_record.word_01 = words[0]

            ## Add the words manually
            for x in range(1,13):
                word_field = 'word_{0:02d}'.format(x)
                setattr(new_record, word_field, words[x -1])

            ## Add the user id manually
            new_record.user = request.user

            ## Save the new instance
            new_record.save()

            ## Construct return (redirect ?) url
            detail_url = target + '_' + stage + '_' + 'detail'

            return redirect(detail_url, id=new_record.id)
    else:
        if stage == 'self':
            form = forms.SelfIdentifierForm()
        elif stage == 'voice':
            form = forms.VoiceIdentifierForm()
        elif stage == 'place':
            form = forms.PlaceIdentifierForm()
        elif stage == 'event':
            form = forms.EventIdentifierForm()
        elif stage == 'object':
            form = forms.ObjectIdentifierForm()
        elif stage == 'person':
            ## The default is handled in the ModelForm class
            # form = forms.PersonIdentifierForm(initial={'dream_gender':'male'})
            form = forms.PersonIdentifierForm()
        else:
            return HttpResponseServerError(stage + ' is not yet supported')



    reports =  []
    words = []
    user = request.user

    '''
    ## Next line returns a QuerySet object
    user_group_ids_qs = user.groups.values_list('pk',flat = True)
    # print('user_group_ids_qs:')
    # pprint(user_group_ids_qs)
    ## Next line returns a list
    user_group_ids = list(user_group_ids_qs)
    print('user_group_ids:',user_group_ids)

    ## Get pk of reports shared specifically to this user and groups this user belongs to
    ## INSERT INTO report_share (report_stage, report_target, report_id, entity_type, entity_id) VALUES ('identifier', 'self', 2, 'user', 3);
    ## INSERT INTO report_share (report_stage, report_target, report_id, entity_type, entity_id) VALUES ('identifier', 'self', 3, 'group', 1);
    ## INSERT INTO report_share (report_stage, report_target, report_id, entity_type, entity_id) VALUES ('illuminator', 'object', 1, 'group', 1);
    shared_report_ids_qs = M_O_D_E_L_S.ReportShare.objects.filter(\
        Q(report_stage=target)\
        &Q(report_target=stage)\
        &(Q(entity_type='user',entity_id=user.pk)\
        |Q(entity_type='group',entity_id__in=user_group_ids)))\
        .values_list('report_id',flat = True)\
        .distinct()

    # print('shared_report_ids_qs:')
    # pprint(shared_report_ids_qs)
    ## Next line returns a list
    shared_report_ids = list(shared_report_ids_qs)
    print('shared_report_ids:',shared_report_ids)
    '''

    # shared_report_ids = get_shared_report_ids(stage, target, user)
    shared_report_ids = get_shared_report_ids(target, stage, user)

    # if target == 'self':
    if stage == 'self':
        ## get all but in random order
        words = M_O_D_E_L_S.SelfWord.objects.all().order_by('?')
        ## get all order by dream_date descending
        # reports = M_O_D_E_L_S.SelfIdentifier.objects.filter(user=user).order_by('-dream_date')
        reports = M_O_D_E_L_S.SelfIdentifier.objects.filter(\
            Q(user=user)\
            |Q(pk__in=shared_report_ids))\
            .order_by('-dream_date')
    elif stage == 'voice':
        ## get all but in random order
        words = M_O_D_E_L_S.VoiceWord.objects.all().order_by('?')
        ## get all order by dream_date descending
        # reports = M_O_D_E_L_S.VoiceIdentifier.objects.filter(user=user).order_by('-dream_date')
        reports = M_O_D_E_L_S.VoiceIdentifier.objects.filter(\
            Q(user=user)\
            |Q(pk__in=shared_report_ids))\
            .order_by('-dream_date')
    elif stage == 'place':
        ## get all but in random order
        words = M_O_D_E_L_S.PlaceWord.objects.all().order_by('?')
        ## get all order by dream_date descending
        # reports = M_O_D_E_L_S.PlaceIdentifier.objects.filter(user=user).order_by('-dream_date')
        reports = M_O_D_E_L_S.PlaceIdentifier.objects.filter(\
            Q(user=user)\
            |Q(pk__in=shared_report_ids))\
            .order_by('-dream_date')
    elif stage == 'event':
        ## get all but in random order
        words = M_O_D_E_L_S.EventWord.objects.all().order_by('?')
        ## get all order by dream_date descending
        # reports = M_O_D_E_L_S.EventIdentifier.objects.filter(user=user).order_by('-dream_date')
        reports = M_O_D_E_L_S.EventIdentifier.objects.filter(\
            Q(user=user)\
            |Q(pk__in=shared_report_ids))\
            .order_by('-dream_date')
    elif stage == 'object':
        ## get all but in random order
        words = M_O_D_E_L_S.ObjectWord.objects.all().order_by('?')
        ## get all order by dream_date descending
        # reports = M_O_D_E_L_S.ObjectIdentifier.objects.filter(user=user).order_by('-dream_date')
        reports = M_O_D_E_L_S.ObjectIdentifier.objects.filter(\
            Q(user=user)\
            |Q(pk__in=shared_report_ids))\
            .order_by('-dream_date')
    elif stage == 'person':
        ## get all but in random order
        words = M_O_D_E_L_S.PersonWord.objects.all().order_by('?')
        ## get all order by dream_date descending
        # reports = M_O_D_E_L_S.PersonIdentifier.objects.filter(user=user).order_by('-dream_date')
        reports = M_O_D_E_L_S.PersonIdentifier.objects.filter(\
            Q(user=user)\
            |Q(pk__in=shared_report_ids))\
            .order_by('-dream_date')
    else:
        return HttpResponseServerError(stage + ' is not yet supported')

    paginator = Paginator(reports, konstants.records_per_page) # Show records_per_page results per page.

    page_number = request.GET.get('page', 1)
    reports_paginated = paginator.get_page(page_number)

    # if target == 'voice':
        #reports = VoiceIdentifier.objects.all().order_by('-dream_date')

    detail_url = target + '_' + stage + '_' + 'detail'

    page_context = {
        'words':words,
        'reports':reports_paginated,
        'target':target,
        'stage':stage,
        'form':form,
        'detail_url':detail_url,
        'action':request.path
    }

    return render(request, 'identifier.html', page_context)

def detail(request, id):
    stage, target, eyed  = request.path.split('/')[-3:]

    report = None
    patterns = None
    methods = None
    descriptions = []
    circle_data = {}

    if target == 'self':
        report = M_O_D_E_L_S.SelfIdentifier.objects.get(pk=id)
        patterns  = konstants.self_patterns
        methods  = konstants.self_methods
    elif target == 'voice':
        report = M_O_D_E_L_S.VoiceIdentifier.objects.get(pk=id)
        patterns  = konstants.voice_patterns
        methods  = konstants.voice_methods
    elif target == 'place':
        report = M_O_D_E_L_S.PlaceIdentifier.objects.get(pk=id)
        patterns  = konstants.place_patterns
        methods  = konstants.place_methods
    elif target == 'event':
        report = M_O_D_E_L_S.EventIdentifier.objects.get(pk=id)
        patterns  = konstants.event_patterns
        methods  = konstants.event_methods
    elif target == 'object':
        report = M_O_D_E_L_S.ObjectIdentifier.objects.get(pk=id)
        patterns  = konstants.object_patterns
        methods  = konstants.object_methods
    elif target == 'person':
        report = M_O_D_E_L_S.PersonIdentifier.objects.get(pk=id)
        patterns  = konstants.person_patterns
        methods  = konstants.person_methods
    else:
        return HttpResponseServerError(target + ' is not yet supported')

    if stage == 'identifier':
        input_count = 12

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

            ## Use django's built in user account system
            user_name = request.user.username
            if target != 'self':
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

            '''
            $sql = "SELECT
            *
            FROM
            {$wpdb->base_prefix}{$this->target}_descriptions_$gender
            WHERE
            arc = '$arc' AND cadence = '$cadence'";
            $records[] = $wpdb->get_row($sql);

            $circleData[$arc][] = $cadence;
            '''
        # END : for x in range(1,input_count + 1)

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

        # this_image = stage + "-target.jpg";
        base_image_partial_path = 'img/' + target + "-target.jpg";
        target_image_partial_url = 'tmp/' + stage + '-' + target + '-' + str(id) + '.jpg'
        ## Oddly enough, there is no elegant way of getting this freaking value
        app_name = request.path.split("/")[1]
        # print(request.path)
        # print(app_name)
        target_image_partial_path = app_name + '/static/' + target_image_partial_url
        target_image_full_path = generate_image_circle(target, circle_data, base_image_partial_path, target_image_partial_path)

        ## Load the image map for tooltip purposes
        map_area_file_name = target_image_full_path.replace('.jpg', '.json')
        print("map_area_file_name =",map_area_file_name)
        with open(map_area_file_name) as maf:
            map_area = json.load(maf)

    # END : if target == 'identifier':




    # START : answer test
    '''
    answers = [
        {'cadence' : 'assert', 'index' : 1, 'text' : 'Persistence while learning from mistakes'},
        {'cadence' : 'assert', 'index' : 5, 'text' : 'When something that inspires me ended up being a failure'},
        {'cadence' : 'assert', 'index' : 6, 'text' : 'Hobby projects'},
        {'cadence' : 'create', 'index' : 2, 'text' : 'When the solution seems open ended'},
        {'cadence' : 'create', 'index' : 5, 'text' : 'Once the results get positive'}
    ]
    '''
    answers = M_O_D_E_L_S.ReportAnswer.objects.filter(\
        report_stage=stage, \
        report_target=target, \
        report_id=id)\
        .order_by('id','cadence','iindex')

    print('answers:')
    pprint(answers)
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

    return render(request, 'identifier_detail.html', page_context)

'''
def test_image_circle(request):
    red = (255,0,0)    # color of our text
    text_pos = (10,10) # top-left position of our text
    text = "Hello World!" # text to draw


    existing_image = Image.open(finders.find('img/self-target.jpg'))
    draw = ImageDraw.Draw(existing_image)
    # font = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 20)

    ## Now, we'll do the drawing:
    # draw.text((0, 0), text, (255, 255, 255), font=font)
    draw.text(text_pos, text, fill=red)

    del draw # I'm done drawing so I don't need this anymore

    ## We need an HttpResponse object with the correct mimetype
    response = HttpResponse(content_type="image/png")
    ## now, we tell the image to save as a PNG to the
    ## provided file-like object
    existing_image.save(response, 'PNG')

    return response
'''

# Method to handle the 'PDF' button click
def pdf(request, id):
    # target, stage, eyed  = request.path.split('/')[-3:]

    request_split = request.path.split('/')
    target, stage = request_split[-4:-2]

    app_name = request_split[1]

    ## Get the full **filesystem**
    ## as the PDF generator does not handle relative web uri
    static_full_path = settings.BASE_DIR + '/' + app_name + '/static'
    pdf_full_path = static_full_path + '/tmp/' + target + '-' + stage + '-' + str(id) + '.pdf'

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
        target, stage = request_split[-4:-2]

        app_name = request_split[1]

        ## Get the full **filesystem**
        ## as the PDF generator does not handle relative web uri
        static_full_path = settings.BASE_DIR + '/' + app_name + '/static'
        pdf_full_path = static_full_path + '/tmp/' + target + '-' + stage + '-' + str(id) + '.pdf'

        # if file exists, return that instead
        pdf_file = Path(pdf_full_path)
        if pdf_file.exists():
            ## No need to do this here :)
            # with open(pdf_full_path, 'rb') as f:
               # pdf_file_data = f.read()

            subject = 'Your Human ' + stage.capitalize() + ' ' + target.capitalize() + ' report in PDF'
            message =  stage.capitalize() + ' ' + target.capitalize()  + ' report and questions'
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

def generate_pdf(page_context):

    # target = page_context.target
    # stage = page_context.stage
    # id = page_context.id
    # app_name = page_context.app_name

    # identifier, illuminator, connector, reflector
    stage = page_context['stage']
    # self, voice, person, place, event, object
    target = page_context['target']
    id = page_context['id']
    app_name = page_context['app_name']

    static_full_path = settings.BASE_DIR + '/' + app_name + '/static'
    # if target == 'connector':
    if stage in ['connector', 'reflector', 'echo']:
        pdf_full_path = static_full_path + '/tmp/' + stage + '-' + str(id) + '.pdf'
    else:
        pdf_full_path = static_full_path + '/tmp/' + stage + '-' + target + '-' + str(id) + '.pdf'

    # if file exists, stop
    pdf_file = Path(pdf_full_path)
    if pdf_file.exists():
        print('there is already a pdf for ' + str(id) + ' at ' + pdf_full_path)
        return

    # report = page_context.report
    # descriptions = page_context.descriptions

    report = page_context['report']
    descriptions = page_context['descriptions']
    # answers = page_context['answers']
    answers = page_context.get('answers', [])

    toc = None
    pdf_pages = []

    image_type = 'circle'
    if stage == 'reflector':
        image_type = 'grid'
        # ... anything else ?

    ## huh ?
    # if target == 'identifier':
        # input_count = 12

    toc = konstants.identifier_illuminator_toc

    try:
        pdf_pages = M_O_D_E_L_S.PdfPage.objects.get(target=target, stage=stage)
    except ObjectDoesNotExist:
        print('No result from PdfPage for target {} and stage {}'.format(target, stage))

    ## Get the full **filesystem** path to the images
    ## as the PDF generator does not handle relative web uri
    report_logo_full_path = static_full_path + '/img/archegyral-orienters-logo-60x60.jpg'
    if stage == 'connector':
        target_stage_image_full_path = static_full_path + '/tmp/connector-' + str(id) + '.jpg'
    elif stage == 'reflector':
        ## not really used in this case
        target_stage_image_full_path = static_full_path + '/tmp/placeholder.jpg'
    elif stage == 'echo':
        target_stage_image_full_path = static_full_path + '/tmp/echo-' + str(id) + '.png'
    else:
        target_stage_image_full_path = static_full_path + '/tmp/' + stage + '-' + target + '-' + str(id) + '.jpg'

    _page_context = {
        'target':target,
        'stage':stage,
        'toc':toc,
        'pdf_pages':pdf_pages,
        'report':report,
        'descriptions':descriptions,
        'answers':answers,
        'image_type':image_type,
        # 'circle_image_url':target_image_partial_url,
        'static_full_path':static_full_path,
        'pdf_full_path':pdf_full_path,
        'report_logo_full_path':report_logo_full_path,
        'target_stage_image_full_path':target_stage_image_full_path,
    }

    ## Admitedly, the folowing looks un-Pythonic & spaghetti-like. Sorry ...
    if stage == 'reflector':
        del _page_context['descriptions']
        _page_context['type'] = target
        _page_context['target'] = "-".join(x.capitalize() for x in target.split("|"))
        _page_context['toc'] = konstants.ing_cadence
        _page_context['aspect_descriptions'] = page_context['aspect_descriptions']
        _page_context['words_left'] = page_context['words_left']
        _page_context['words_right'] = page_context['words_right']
        _page_context['ing_cadence'] = page_context['ing_cadence']

        if target == "self|self":
            _page_context['archetype_images'] = page_context['archetype_images']
        else:
            _page_context['archetype_images1'] = page_context['archetype_images1']
            _page_context['archetype_images2'] = page_context['archetype_images2']
            _page_context['first_name1'] = page_context['first_name1']
            _page_context['first_name2'] = page_context['first_name2']

    if stage == 'echo':
        ## Yes, the following is what the PHP version does
        pdf_pages = M_O_D_E_L_S.PdfPage.objects.get(target='self', stage='identifier')
        _page_context['toc'] = []
        _page_context['submissions'] = page_context['submissions']
        _page_context['pdf_pages'] = pdf_pages

    # getting the template
    render_result = render_to_pdf(stage + '_pdf.html', _page_context)

    if render_result:
        with open(pdf_full_path, 'rb') as f:
           pdf_file_data = f.read()

        print("pdf for " + str(id) + " generated at " + pdf_full_path)
    else:
        print("unable to generate pdf for " + str(id) + " at " + pdf_full_path)

def generate_image_circle(target, circle_data, base_image_partial_path, target_image_partial_path):
    # TODO : possible to not have to specify the app name below ?
    target_image_full_path = settings.BASE_DIR + '/' + target_image_partial_path

    # if file exists, bail
    target_image_file = Path(target_image_full_path)
    if target_image_file.exists():
        print(target_image_full_path,"already exists. not generating new image ...")
        return target_image_full_path

    en_data = {}
    if target == 'self':
        en_data = konstants.get_en_data(konstants.self_patterns)
    elif target == 'voice':
        en_data = konstants.get_en_data(konstants.voice_patterns)
    elif target == 'place':
        en_data = konstants.get_en_data(konstants.place_patterns)
    elif target == 'event':
        en_data = konstants.get_en_data(konstants.event_patterns)
    elif target == 'object':
        en_data = konstants.get_en_data(konstants.object_patterns)
    elif target == 'person':
        en_data = konstants.get_en_data(konstants.person_patterns)
    else:
        return HttpResponseServerError(target + ' is not yet supported')

    existing_image = Image.open(finders.find(base_image_partial_path))
    draw = ImageDraw.Draw(existing_image)
    # font = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 20)
    font = ImageFont.truetype(
        # 'Ubuntu-B.ttf',
        'DejaVuSans.ttf',
        18)

    map_area = []
    # map_area = {}

    ## Now, we'll do the drawing:
    # foreach ($data as $arc => $array)
    for key, values in circle_data.items():
        print(key)
        ## 0 : black, 1 : white
        text_color =  (255, 255, 255) if en_data.get(key)['color'] == 1 else (0, 0, 0)

        offset = 0;
        # foreach ($array as $cadence)
        for value in values:
            print('-' + value)
            # imagestring ($image, 5, $enData[$arc]['x'], $enData[$arc]['y'] + $offset++ * 15, $cadence, $textColor);
            text_pos = (en_data[key]['x'], en_data[key]['y'] + offset * 15)
            offset += 1
            draw.text(text_pos, value, fill=text_color, font=font)
            # Get text rectangle bound
            text_size = font.getsize(value)
            coords = [text_pos[0], text_pos[1], text_pos[0] + text_size[0], text_pos[1] + text_size[1]]
            map_area.append({'cadence':value,'coords':coords})

    del draw # I'm done drawing so I don't need this anymore

    file=open(target_image_full_path,"w+")
    existing_image.save(file)
    file.close()

    print("map_area =")
    pprint(map_area)

    ## Save map_area for subsequent viewing
    map_area_file_name = target_image_full_path.replace('.jpg', '.json')
    with open(map_area_file_name, 'w') as maf:
        maf.write(json.dumps(map_area))

    return target_image_full_path
