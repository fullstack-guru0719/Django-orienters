from io import BytesIO

from django.http import HttpResponse
from django.template.loader import get_template

#pisa is a html2pdf converter using the ReportLab Toolkit,
#the HTML5lib and pyPdf.

from xhtml2pdf import pisa
#difine render_to_pdf() function

from html.parser import HTMLParser

from django.db.models import Q
from . import models as M_O_D_E_L_S

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    # print("~~~~~~~~ html",html)
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def render_to_pdf(template_src, context_dict={}):
    # print(context_dict)

    pdf_full_path = context_dict['pdf_full_path']

    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()

    ##b This part will create the pdf.
    # pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    pdf = pisa.pisaDocument(BytesIO(html.encode('utf-8')), result)
    if not pdf.err:
        # save to file
        with open(pdf_full_path, 'wb') as f:
            f.write(result.getvalue())
        # return response
        # return HttpResponse(result.getvalue(), content_type='application/pdf')
        return True
    return False
    # return None

def get_gender(request):
    gender = 'male'
    if hasattr(request.user, 'human'):
        gender = request.user.human.gender

    return gender

# get_shared_report_ids('identifier', 'self', user)
def get_shared_report_ids(stage, target, user):
    ## Next line returns a QuerySet object
    user_group_ids_qs = user.groups.values_list('pk',flat = True)
    ## Next line returns a list
    user_group_ids = list(user_group_ids_qs)
    print('user_group_ids:',user_group_ids)

    ## Get pk of reports shared specifically to this user and groups this user belongs to
    if target is None:
        shared_report_ids_qs = M_O_D_E_L_S.ReportShare.objects.filter(\
            Q(report_stage=stage)\
            &(Q(entity_type='user',entity_id=user.pk)\
            |Q(entity_type='group',entity_id__in=user_group_ids)))\
            .values_list('report_id',flat = True)\
            .distinct()
    else:
        shared_report_ids_qs = M_O_D_E_L_S.ReportShare.objects.filter(\
            Q(report_stage=stage)\
            &Q(report_target=target)\
            &(Q(entity_type='user',entity_id=user.pk)\
            |Q(entity_type='group',entity_id__in=user_group_ids)))\
            .values_list('report_id',flat = True)\
            .distinct()

    ## Next line returns a list
    shared_report_ids = list(shared_report_ids_qs)
    print('shared_report_ids:',shared_report_ids)

    return shared_report_ids

def shared_reports_by_user(request, user):
    ## Part 1 : identifier
    identifier_self_reports = []
    identifier_voice_reports = []
    identifier_place_reports = []
    identifier_event_reports = []
    identifier_object_reports = []
    identifier_person_reports = []

    if user.pk == request.user.pk:
        identifier_self_reports = M_O_D_E_L_S.SelfIdentifier.objects.filter(user=user).values('id','dream_name','dream_date').order_by('-dream_date')
        identifier_voice_reports = M_O_D_E_L_S.VoiceIdentifier.objects.filter(user=user).values('id','dream_name','dream_date').order_by('-dream_date')
        identifier_place_reports = M_O_D_E_L_S.PlaceIdentifier.objects.filter(user=user).values('id','dream_name','dream_date').order_by('-dream_date')
        identifier_event_reports = M_O_D_E_L_S.EventIdentifier.objects.filter(user=user).values('id','dream_name','dream_date').order_by('-dream_date')
        identifier_object_reports = M_O_D_E_L_S.ObjectIdentifier.objects.filter(user=user).values('id','dream_name','dream_date').order_by('-dream_date')
        identifier_person_reports = M_O_D_E_L_S.PersonIdentifier.objects.filter(user=user).values('id','dream_name','dream_date').order_by('-dream_date')
    else :
        shared_report_ids = get_shared_report_ids('identifier', 'self', request.user)
        identifier_self_reports = M_O_D_E_L_S.SelfIdentifier.objects.filter(\
            Q(user=user)\
            &Q(pk__in=shared_report_ids))\
            .values('id','dream_name','dream_date')\
            .order_by('-dream_date')

        shared_report_ids = get_shared_report_ids('identifier', 'voice', request.user)
        identifier_voice_reports = M_O_D_E_L_S.VoiceIdentifier.objects.filter(\
            Q(user=user)\
            &Q(pk__in=shared_report_ids))\
            .values('id','dream_name','dream_date')\
            .order_by('-dream_date')

        shared_report_ids = get_shared_report_ids('identifier', 'place', request.user)
        identifier_place_reports = M_O_D_E_L_S.PlaceIdentifier.objects.filter(\
            Q(user=user)\
            &Q(pk__in=shared_report_ids))\
            .values('id','dream_name','dream_date')\
            .order_by('-dream_date')

        shared_report_ids = get_shared_report_ids('identifier', 'event', request.user)
        identifier_event_reports = M_O_D_E_L_S.EventIdentifier.objects.filter(\
            Q(user=user)\
            &Q(pk__in=shared_report_ids))\
            .values('id','dream_name','dream_date')\
            .order_by('-dream_date')

        shared_report_ids = get_shared_report_ids('identifier', 'object', request.user)
        identifier_object_reports = M_O_D_E_L_S.ObjectIdentifier.objects.filter(\
            Q(user=user)\
            &Q(pk__in=shared_report_ids))\
            .values('id','dream_name','dream_date')\
            .order_by('-dream_date')

        shared_report_ids = get_shared_report_ids('identifier', 'person', request.user)
        identifier_person_reports = M_O_D_E_L_S.PersonIdentifier.objects.filter(\
            Q(user=user)\
            &Q(pk__in=shared_report_ids))\
            .values('id','dream_name','dream_date')\
            .order_by('-dream_date')
    ## end : if user.pk == request.user.pk:

    for i in identifier_self_reports:
        i['stage'] = 'identifier'
        i['target'] = 'self'

    for i in identifier_voice_reports:
        i['stage'] = 'identifier'
        i['target'] = 'voice'

    for i in identifier_place_reports:
        i['stage'] = 'identifier'
        i['target'] = 'place'

    for i in identifier_event_reports:
        i['stage'] = 'identifier'
        i['target'] = 'event'

    for i in identifier_object_reports:
        i['stage'] = 'identifier'
        i['target'] = 'object'

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


    ## Part 2 : illuminator
    illuminator_self_reports = []
    illuminator_voice_reports = []
    illuminator_place_reports = []
    illuminator_event_reports = []
    illuminator_object_reports = []
    illuminator_person_reports = []

    if user.pk == request.user.pk:
        illuminator_self_reports = M_O_D_E_L_S.SelfIlluminator.objects.filter(user=user).values('id','dream_name','dream_date').order_by('-dream_date')
        illuminator_voice_reports = M_O_D_E_L_S.VoiceIlluminator.objects.filter(user=user).values('id','dream_name','dream_date').order_by('-dream_date')
        illuminator_place_reports = M_O_D_E_L_S.PlaceIlluminator.objects.filter(user=user).values('id','dream_name','dream_date').order_by('-dream_date')
        illuminator_event_reports = M_O_D_E_L_S.EventIlluminator.objects.filter(user=user).values('id','dream_name','dream_date').order_by('-dream_date')
        illuminator_object_reports = M_O_D_E_L_S.ObjectIlluminator.objects.filter(user=user).values('id','dream_name','dream_date').order_by('-dream_date')
        illuminator_person_reports = M_O_D_E_L_S.PersonIlluminator.objects.filter(user=user).values('id','dream_name','dream_date').order_by('-dream_date')
    else:
        shared_report_ids = get_shared_report_ids('illuminator', 'self', request.user)
        illuminator_self_reports = M_O_D_E_L_S.SelfIlluminator.objects.filter(\
            Q(user=user)\
            &Q(pk__in=shared_report_ids))\
            .values('id','dream_name','dream_date')\
            .order_by('-dream_date')

        shared_report_ids = get_shared_report_ids('illuminator', 'voice', request.user)
        illuminator_voice_reports = M_O_D_E_L_S.VoiceIlluminator.objects.filter(\
            Q(user=user)\
            &Q(pk__in=shared_report_ids))\
            .values('id','dream_name','dream_date')\
            .order_by('-dream_date')

        shared_report_ids = get_shared_report_ids('illuminator', 'place', request.user)
        illuminator_place_reports = M_O_D_E_L_S.PlaceIlluminator.objects.filter(\
            Q(user=user)\
            &Q(pk__in=shared_report_ids))\
            .values('id','dream_name','dream_date')\
            .order_by('-dream_date')

        shared_report_ids = get_shared_report_ids('illuminator', 'event', request.user)
        illuminator_event_reports = M_O_D_E_L_S.EventIlluminator.objects.filter(\
            Q(user=user)\
            &Q(pk__in=shared_report_ids))\
            .values('id','dream_name','dream_date')\
            .order_by('-dream_date')

        shared_report_ids = get_shared_report_ids('illuminator', 'object', request.user)
        illuminator_object_reports = M_O_D_E_L_S.ObjectIlluminator.objects.filter(\
            Q(user=user)\
            &Q(pk__in=shared_report_ids))\
            .values('id','dream_name','dream_date')\
            .order_by('-dream_date')

        shared_report_ids = get_shared_report_ids('illuminator', 'person', request.user)
        illuminator_person_reports = M_O_D_E_L_S.PersonIlluminator.objects.filter(\
            Q(user=user)\
            &Q(pk__in=shared_report_ids))\
            .values('id','dream_name','dream_date')\
            .order_by('-dream_date')
    ## end : if user.pk == request.user.pk:

    for i in illuminator_self_reports:
        i['stage'] = 'illuminator'
        i['target'] = 'self'

    for i in illuminator_voice_reports:
        i['stage'] = 'illuminator'
        i['target'] = 'voice'

    for i in illuminator_place_reports:
        i['stage'] = 'illuminator'
        i['target'] = 'place'

    for i in illuminator_event_reports:
        i['stage'] = 'illuminator'
        i['target'] = 'event'

    for i in illuminator_object_reports:
        i['stage'] = 'illuminator'
        i['target'] = 'object'

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

    ## construct our custom dict (?)
    result = {
        'id' : user.id,
        'first_name' : user.first_name,
        'last_name' : user.last_name,
        'username' : user.username,
        'identifier_reports' : identifier_reports,
        'illuminator_reports' : illuminator_reports}

    return result
