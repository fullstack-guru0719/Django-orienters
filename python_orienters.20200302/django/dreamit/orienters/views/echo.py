import sys
import json
import math
import requests

# from django.db.models import Count, Q
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse, HttpResponseServerError
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.urls import reverse

from inflector import Inflector, English
from similar_text import similar_text

from pathlib import Path
from pprint import pprint

from .. import forms
from .. import konstants
from .. import models as M_O_D_E_L_S
from ..utils import render_to_pdf, get_gender
from .identifier import generate_pdf

@login_required
def index(request):
    eyed = None

    if request.method == 'POST':
        # eyed = request.POST.get('id', None)
        eyed = request.POST.get('id', '')

        print("request.POST.get('id') =",eyed)

        if eyed != '':
            instance = M_O_D_E_L_S.Echo.objects.get(pk=eyed)
            form = forms.EchoForm(request.POST or None, instance=instance)
        else:
            form = forms.EchoForm(request.POST)

        if form.is_valid():
            # print("saving form submission (?)")
            new_record = form.save()
            ## Re-init form after save with values from the database.
            ## This ensures that "form.group.value" gets set properly.
            form = forms.EchoForm(instance=M_O_D_E_L_S.Echo.objects.get(pk=new_record.pk))
        else:
            print("sorry, can't save")

    else:
        form = forms.EchoForm()

    user = request.user
    groups = Group.objects.all()

    # reports = M_O_D_E_L_S.Echo.objects.filter(group__in=user.groups).order_by('-id')[:20]
    reports = M_O_D_E_L_S.Echo.objects.filter(group__in=user.groups.values_list('pk',flat = True)).order_by('-id')[:20]

    paginator = Paginator(reports, konstants.records_per_page) # Show records_per_page results per page.

    page_number = request.GET.get('page', 1)
    reports_paginated = paginator.get_page(page_number)

    page_context = {
        'reports' : reports_paginated,
        'detail_url' : 'echo_detail',
        'answer_url' : 'echo_answer',
    }

    return render(request, 'echo.html', page_context)

@login_required
def answer(request, id):

    source_echo = M_O_D_E_L_S.Echo.objects.get(pk=id)
    echo = None
    page_context = {}
    template = None

    if request.method == 'POST':
        type = request.POST.get('type', 'self')

        eyed = request.POST.get('id', '')
        input_count = request.POST.get('input_count', 0)
        input_keywords = request.POST.get('input_keywords', '')
        # input_data = request.POST.get('answer', '')
        input_data = request.POST.get('input_data', '')

        # if type == 'self':

        if eyed == '':
            echo = M_O_D_E_L_S.SelfEcho( \
                # group=group_id, \
                echo=source_echo, \
                user=request.user, \
                input_count=input_count, \
                input_keywords=input_keywords, \
                input_data=input_data)
            echo.save()
        else:
            echo = M_O_D_E_L_S.SelfEcho.objects.get(pk=eyed)
            if echo is not None:
                ## Update the record
                echo.input_count = input_count
                echo.input_keywords = input_keywords
                echo.input_data = input_data
                echo.save()

        ## Now process the words ...

        ## START : inspired by the Illuminator
        ## Get all illuminator words
        words = M_O_D_E_L_S.IlluminatorWord.objects.all()

        ## Init the Inflector with English
        enflector = Inflector(English)

        input_keywords_split = input_keywords.split('|')

        for index, input_keyword in enumerate(input_keywords_split):
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
            setattr(echo, word_field, quality)

            print('{} : {} => {}'.format(index, input_keyword, quality))
        ## end : for index, input_keyword in enumerate(input_keywords):

        ## Don't forget to persist :)
        echo.save()
        ## END : inspired by the Illuminator

        template = 'echo_thank_you.html'
    else:
        # Has this been answered before ?
        try:
            echo = M_O_D_E_L_S.SelfEcho.objects.filter(echo=source_echo,user=request.user)[:1].get()
        except ObjectDoesNotExist:
            # raise Http404
            print('Echo {} has not yet been answered by {}'.format(id,request.user.username))

        back_url = 'echo_index'
        # pdf_url = 'echo_pdf'

        if 'HTTP_REFERER' in request.META:
            ## Next line includes paging status :D
            back_url = request.META['HTTP_REFERER']

        page_context = {
            'source_echo':source_echo,
            'echo':echo,
            'answer_url':'echo_answer',
            'back_url':back_url
        }

        template = 'echo_answer.html'
    ## end : if request.method == 'POST':

    ## Remove existing PNG & PDF so that updated ones can be
    ## generated once the next "detail view" request comes
    remove_existing_generated_assets(request, id)

    return render(request, template, page_context)

@login_required
def detail(request, id):
    source_echo = M_O_D_E_L_S.Echo.objects.get(pk=id)
    echo = None
    error_message = ''
    zData = []
    descriptions = []

    try:
        echo = M_O_D_E_L_S.SelfEcho.objects.filter(echo=source_echo,user=request.user)[:1].get()
    except ObjectDoesNotExist:
        # raise Http404
        error_message = 'Echo {} has not yet been answered by {}'.format(id,request.user.username)
        print(error_message)

    if echo is not None:
    	## calculate data for the current user/post. See line 292 in www/wp-content/plugins/dreamit-echos.php
        z_data_element = calculate_zdata(echo)
        zData.append(z_data_element)

        gender = get_gender(request)
        patterns  = konstants.self_patterns
        methods  = konstants.self_methods

        ## The old code. See line 333 in www/wp-content/plugins/dreamit-echos.php
        ## Visible in PDF only
        for i in range(1,echo.input_count + 1):
            word_field = 'word_{0:02d}'.format(i)
            word_field_value = getattr(echo, word_field)
            archetype = patterns[word_field_value % echo.input_count]
            cadence = methods[i]

            if gender == 'male':
                qs = M_O_D_E_L_S.SelfDescriptionMale.objects.filter(archetype=archetype, cadence=cadence)
            else:
                qs = M_O_D_E_L_S.SelfDescriptionFemale.objects.filter(archetype=archetype, cadence=cadence)

            # descriptions.append(list(qs))

            user_name = request.user.username

            for q in qs:
                # descriptions.append(q)
                q_mod = q

                report_str = q.report
                report_str_mod_1 = report_str.replace('[name]', user_name)
                report_str_mod_2 = report_str_mod_1.replace('[situation]', source_echo.name)
                q_mod.report = report_str_mod_2

                descriptions.append(q_mod)
            ## end : for q in qs:
    ## end : if echo is not None:

    echoes = None
    try:
        echoes = M_O_D_E_L_S.SelfEcho.objects.filter(echo=source_echo).exclude(user=request.user)
    except ObjectDoesNotExist:
        # raise Http404
        error_message = 'Echo {} has not been answered by others'.format(id)
        print(error_message)

    if echoes is not None:
        for ee in echoes:
	        ## Get other results for the same echo. See line 313 in www/wp-content/plugins/dreamit-echos.php
            z_data_element = calculate_zdata(ee)
            zData.append(z_data_element)
        ## end : for echo in echoes:
    ## end : if echoes is not None:

    ## START : chart related
    ## The PDF only needs the x & y co-ords as the tooltip feature is irrelevant here
    x_y_only = [{'x':xx.get('x'), 'y':xx.get('y')} for xx in zData]
    pdf_chart_options = construct_chart_options(x_y_only)

    template_chart_options = construct_chart_options(zData)
    ## END : chart related

    ## START : PDF image generation
    target_image_partial_url = 'tmp/echo-' + str(id) + '.png'
    ## Oddly enough, there is no elegant way of getting this freaking value
    app_name = request.path.split("/")[1]
    # print(request.path)
    # print(app_name)
    target_image_partial_path = app_name + '/static/' + target_image_partial_url
    target_image_full_path = generate_image_via_highcharts(pdf_chart_options, target_image_partial_path)
    ## END : PDF image generation

    pdf_context = {
        'circle_image_url':target_image_full_path,
        'report':echo,
        'descriptions':descriptions,
        'submissions':zData,
        'chart_options':pdf_chart_options,
        'target': source_echo.type,
        'stage': 'echo',
        ## sharing feature
        # 'groups':groups,
        # 'users':users,
        'user_id':request.user.id,
        ## uri
        # 'pdf_url':pdf_url,
        # 'back_url':back_url,
        ## the following are for generating the pdf
        # 'id': echo.id,
        'id': source_echo.id,
        'app_name':app_name,
    }

    generate_pdf(pdf_context)

    page_context = {
        'id':id,
        'source_echo':source_echo,
        'echo':echo,
        'error_message':error_message,
        'submissions':zData,
        'chart_options':template_chart_options,
        'descriptions':descriptions
    }

    return render(request, 'echo_detail.html', page_context)

def calculate_zdata(echo):
    # x = (echo.word_01 * 30) - 15 + (echo.word_02 ? (echo.word_02 - echo.word_01) : 0)
    diff = 0
    if echo.word_02:
        diff = echo.word_02 - echo.word_01
    x = (echo.word_01 * 30) - 15 + diff

    sum_numbers = 0
    for i in range(1,echo.input_count + 1):
        word_field = 'word_{0:02d}'.format(i)
        word_field_value = getattr(echo, word_field)
        sum_numbers += word_field_value

    y = (sum_numbers / 12) + 1

    return {
        'x' : round((x - 15)/30, 2),
        'y' : round(y, 2),
        'text' : echo.input_data,
        # 'user' : User.objects.get(id=echo.user)
        # 'user' : echo.user,
        'user' : echo.user.first_name + ' ' + echo.user.last_name,
        # 'created_at' : echo.created_at
        'created_at' : "{:%I:%M %p, %d %B %Y}".format(echo.created_at)
    }

def construct_chart_options(submissions):
    chart_options = """{

chart: {
    polar: true
},

title: {
    text: 'Self Echo'
},

xAxis: {
    tickInterval: 1,
	min: 0,
	max: 12,
	reversed: true,
	categories: ['START-UP', 'ORGANIC', 'DOCUMENTARY', 'CLAN', 'MAJESTIC', 'FACTUAL', 'DIPLOMATIC', 'CLANDESTINE', 'MYTHICAL', 'ESTABLISHMENT', 'AVANT-GARDE', 'FABLED'],
	labels: {
		style: {
			fontWeight: 'bold'
		}
	}
},

yAxis: {
    min: 0,
	gridLineWidth: 0,
	labels: {enabled: false}
},

plotOptions: {
    series: {
		pointStart: 0,
		pointInterval: 1,
		states: {
            hover: {
                enabled:false
            }
        }
	},
	column: {
		pointPadding: 0,
		groupPadding: 0
	},
	line: {
		connectEnds: false,
		lineWidth: 0
	}
},

series: [{
    type: 'line',
	name: 'Line',
    data: %s,
    color: '#7F007F',
	stickyTracking: false
}],

exporting: {
    buttons: {
        contextButton: {
            enabled: false
        }
    }
},

legend:{
	enabled: false
},

tooltip: {
	shape: 'square',
	style: {'whiteSpace': 'normal !important', 'height': 'auto', 'width': '350px'},
	formatter: function() {
		return this.point.text;
	}
}

}"""
    mod_chart_options = chart_options % (json.dumps(submissions))
    return mod_chart_options

def remove_existing_generated_assets(request, id):
    ## Oddly enough, there is no elegant way of getting this freaking value
    app_name = request.path.split("/")[1]

    ## remove PNG
    target_image_partial_url = 'tmp/echo-' + str(id) + '.png'
    target_image_partial_path = app_name + '/static/' + target_image_partial_url
    target_image_full_path = settings.BASE_DIR + '/' + target_image_partial_path

    target_image_file = Path(target_image_full_path)
    if target_image_file.exists():
        target_image_file.unlink()

    ## remove PDF
    target_pdf_partial_url = 'tmp/echo-' + str(id) + '.pdf'
    target_pdf_partial_path = app_name + '/static/' + target_pdf_partial_url
    target_pdf_full_path = settings.BASE_DIR + '/' + target_pdf_partial_path

    target_pdf_file = Path(target_pdf_full_path)
    if target_pdf_file.exists():
        target_pdf_file.unlink()

def generate_image_via_highcharts(pdf_chart_options, target_image_partial_path):
    # TODO : possible to not have to specify the app name below ?
    target_image_full_path = settings.BASE_DIR + '/' + target_image_partial_path

    # if file exists, bail
    target_image_file = Path(target_image_full_path)
    if target_image_file.exists():
        print(target_image_full_path,"already exists. not generating new image ...")
        return target_image_full_path

    headers = {'Accept': 'image/png', 'content-type': 'application/json'}
    data = {
      "options":pdf_chart_options,
      "type": "image/png",
      "filename":"dummy.png"
    }

    r = requests.post('http://export.highcharts.com/',
        data=json.dumps(data),
        headers=headers,
        verify=False)

    open(target_image_full_path, 'wb').write(r.content)

    return target_image_full_path

# Method to handle the 'PDF' button click
def pdf(request, id):
    # target, stage, eyed  = request.path.split('/')[-3:]

    request_split = request.path.split('/')
    # target, stage = request_split[-4:-2]

    app_name = request_split[1]

    ## Get the full **filesystem**
    ## as the PDF generator does not handle relative web uri
    static_full_path = settings.BASE_DIR + '/' + app_name + '/static'
    pdf_full_path = static_full_path + '/tmp/echo-' + str(id) + '.pdf'

    # if file exists, return that instead
    pdf_file = Path(pdf_full_path)
    if pdf_file.exists():
        with open(pdf_full_path, 'rb') as f:
           pdf_file_data = f.read()

        return HttpResponse(pdf_file_data, content_type='application/pdf')
    else:
        return HttpResponseServerError(pdf_full_path + ' does not exists')
