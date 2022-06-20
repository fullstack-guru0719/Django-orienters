import sys

# from django.db.models import Count, Q
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group, User
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse, HttpResponseServerError
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.urls import reverse

from pprint import pprint

from .. import forms
from .. import konstants
from .. import models as M_O_D_E_L_S

def index(request):
    return HttpResponse("Hello, world. You're at the admin index.")

@login_required
def login_success(request):
    if request.user.is_superuser:
        # user is an admin
        return redirect("pdf_pages_identifier_self")
    else:
        return redirect("identifier_self")


@login_required
def manage_groups(request):

    ## TODO : complete me

    groups = Group.objects.all()
    users = User.objects.all().exclude(is_superuser=1)

    page_context = {
        'groups':groups,
        'users':users}

    return render(request, 'admin/groups.html', page_context)

# @login_required
@user_passes_test(lambda u: u.is_superuser)
def manage_echoes(request):
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

    groups = Group.objects.all()

    reports = M_O_D_E_L_S.Echo.objects.all().order_by('-id')[:20]

    paginator = Paginator(reports, konstants.records_per_page) # Show records_per_page results per page.

    page_number = request.GET.get('page', 1)
    reports_paginated = paginator.get_page(page_number)

    page_context = {
        'id':eyed,
        # 'echo':echo,
        'form':form,
        'groups' : groups,
        'reports' : reports_paginated,
        'edit_url' : 'edit_echo',
        ## TODO : use actual url (which is the same as the one users see after they answer the Echo's question)
        'view_url' : 'echo_detail'
    }

    return render(request, 'admin/echoes.html', page_context)

# @login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_echo(request, id):
    instance = M_O_D_E_L_S.Echo.objects.get(pk=id)
    form = forms.EchoForm(request.POST or None, instance=instance)

    groups = Group.objects.all()

    reports = M_O_D_E_L_S.Echo.objects.all().order_by('-id')[:20]

    paginator = Paginator(reports, konstants.records_per_page) # Show records_per_page results per page.

    page_number = request.GET.get('page', 1)
    reports_paginated = paginator.get_page(page_number)

    back_url = reverse('manage_echoes')

    if 'HTTP_REFERER' in request.META:
        ## Next line includes paging status :D
        back_url = request.META['HTTP_REFERER']

    page_context = {
        'id':id,
        # 'echo':echo,
        'form':form,
        'groups' : groups,
        'reports' : reports_paginated,
        'edit_url' : 'edit_echo',
        ## TODO : use actual url (which is the same as the one users see after they answer the Echo's question)
        'view_url' : 'edit_echo',
        'back_url' : back_url
    }

    return render(request, 'admin/echoes.html', page_context)


# @login_required
@user_passes_test(lambda u: u.is_superuser)
def pdf_pages(request):
    stage, target  = request.path.split('/')[-2:]

    print("stage, target =",stage,target)

    if request.method == 'POST':

        print("request.POST.get('id') =",request.POST.get('id'))

        instance = M_O_D_E_L_S.PdfPage.objects.get(pk=request.POST.get('id'))
        form = forms.PdfPageForm(request.POST or None, instance=instance)
        if form.is_valid():
            form.save()

    ## end : if request.method == 'POST':

    # get the first found record
    pdf_page = M_O_D_E_L_S.PdfPage.objects.filter(stage=stage,target=target).first()

    page_context = {
        'stage':stage,
        'target':target,
        'pdf_page':pdf_page}

    return render(request, 'admin/pdf_pages.html', page_context)
