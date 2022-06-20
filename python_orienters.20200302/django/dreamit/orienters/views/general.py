import sys

from django.shortcuts import render, redirect
from django.conf import settings

# Create your views here.
from django.http import JsonResponse, HttpResponse, HttpResponseServerError

# importing get_template from loader
from django.template.loader import get_template

from .. import models as M_O_D_E_L_S

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def login(request):
    page_context = {}

    return render(request, 'login.html', page_context)

## How I created myself
# def create_user(request):
#    user = get_user_model().objects.create_user(
#        username='peter',
#        email='peter.govind.jr@gmail.com',
#        password='p')
#    return HttpResponse(user.id)

def share_report(request):

    if request.method != 'POST':
        return HttpResponseServerError('unsupported method')

    print('share_report:')
    for key, values in request.POST.lists():
        print(key, values)

    reports = []
    for key, values in request.POST.lists():
        if key.startswith('user-'):
            # reports.append(values);
            reports.append(values[0]);

    ## Let's go manual rather than use Django's Form thingy
    report_stage = request.POST.get('stage', 'identifier')
    report_target = request.POST.get('target', 'self')
    report_id = request.POST.get('id')

    user_ids = request.POST.getlist('share_with_user_id', [])
    group_ids = request.POST.getlist('share_with_group_id', [])

    ## remove existing share records for this report
    M_O_D_E_L_S.ReportShare.objects.filter(\
        report_stage=report_stage, \
        report_target=report_target, \
        report_id=report_id).delete()

    if len(user_ids) == 0 and len(group_ids) == 0:
        message = 'Please select who you want to share this report with'

    data = {}
    results = []

    if len(user_ids) > 0:
        for user_id in user_ids:
            rs = M_O_D_E_L_S.ReportShare(\
                report_stage=report_stage, \
                report_target=report_target, \
                report_id=report_id, \
                entity_type='user', \
                entity_id=user_id)
            rs.save()
            results.append(rs.pk)

    if len(group_ids) > 0:
        for group_id in group_ids:
            rs = M_O_D_E_L_S.ReportShare(\
                report_stage=report_stage, \
                report_target=report_target, \
                report_id=report_id, \
                entity_type='group', \
                entity_id=group_id)
            rs.save()
            results.append(rs.pk)

    if len(results) > 0:
        data = {
            'status' : 'ok',
            'message': results
        }
    else:
        data = {
            'status' : 'error',
            'message': message
        }

    return JsonResponse(data)

def answer_report(request):

    if request.method != 'POST':
        return HttpResponseServerError('unsupported method')

    print('answer_report:')
    for key, values in request.POST.lists():
        print(key, values)

    ## Let's go manual rather than use Django's Form thingy
    report_stage = request.POST.get('stage', 'identifier')
    report_target = request.POST.get('target', 'self')
    report_id = request.POST.get('id')
    cadence = request.POST.get('cadence')
    iindex = request.POST.get('iindex')
    text = request.POST.get('text', '')


    data = {}
    results = []

    ## remove existing answer for this question
    M_O_D_E_L_S.ReportAnswer.objects.filter(\
        report_stage=report_stage, \
        report_target=report_target, \
        report_id=report_id, \
        cadence=cadence, \
        iindex=iindex).delete()

    ## then save the new one, if it's not empty
    if (text is not ''):
        rs = M_O_D_E_L_S.ReportAnswer(\
            report_stage=report_stage, \
            report_target=report_target, \
            report_id=report_id, \
            cadence=cadence, \
            iindex=iindex, \
            text=text)
        rs.save()
        results.append(rs.pk)

    data = {
        'status' : 'ok',
        'message': results
    }

    return JsonResponse(data)

## http://localhost:8000/orienters/general/gen_sql
def gen_sql(request):
    request_split = request.path.split('/')
    app_name = request_split[1]

    kount = 0

    ## --------------

    # table_name = M_O_D_E_L_S.SelfDescriptionMale._meta.db_table
    rows = M_O_D_E_L_S.SelfDescriptionMale.objects.all()
    kount += _gen_sql(app_name, rows)

    rows = M_O_D_E_L_S.SelfDescriptionFemale.objects.all()
    kount += _gen_sql(app_name, rows)

    ## --------------

    rows = M_O_D_E_L_S.VoiceDescriptionMale.objects.all()
    kount += _gen_sql(app_name, rows)

    rows = M_O_D_E_L_S.VoiceDescriptionFemale.objects.all()
    kount += _gen_sql(app_name, rows)

    ## --------------

    rows = M_O_D_E_L_S.PlaceDescriptionMale.objects.all()
    kount += _gen_sql(app_name, rows)

    rows = M_O_D_E_L_S.PlaceDescriptionFemale.objects.all()
    kount += _gen_sql(app_name, rows)

    ## --------------

    rows = M_O_D_E_L_S.EventDescriptionMale.objects.all()
    kount += _gen_sql(app_name, rows)

    rows = M_O_D_E_L_S.EventDescriptionFemale.objects.all()
    kount += _gen_sql(app_name, rows)

    ## --------------

    rows = M_O_D_E_L_S.ObjectDescriptionMale.objects.all()
    kount += _gen_sql(app_name, rows)

    rows = M_O_D_E_L_S.ObjectDescriptionFemale.objects.all()
    kount += _gen_sql(app_name, rows)

    ## --------------

    rows = M_O_D_E_L_S.PersonDescriptionMale.objects.all()
    kount += _gen_sql(app_name, rows)

    rows = M_O_D_E_L_S.PersonDescriptionFemale.objects.all()
    kount += _gen_sql(app_name, rows)

    ## --------------

    return JsonResponse({'status':kount})

def _gen_sql(app_name, rows):
    table_name = rows[0]._meta.db_table

    ss = [];
    for row in rows:
        s = 'UPDATE ' + table_name + ' SET report = \'' + row.report + '\' \nWHERE id = ' + str(row.pk) + ';'
        ss.append(s)

    ## Construct the full **filesystem** destination
    static_full_path = settings.BASE_DIR + '/' + app_name + '/static'
    sql_full_path = static_full_path + '/sql/' + table_name + '.sql'

    line_counter = 1
    with open(sql_full_path, 'w') as f:
        for s in ss:
            f.write("%s\n" % s)
            if line_counter == 12:
                line_counter = 1
                f.write("\n\n\n")
            else:
                line_counter += 1

    return len(ss)
