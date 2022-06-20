from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from django.urls import path

# from . import views as v

from .views import custom_admin
from .views import general
from .views import identifier
from .views import illuminator
from .views import connector
from .views import reflector
from .views import echo

urlpatterns = [
    path('', general.index, name='index'),

    ## next is an Ajax endpoint
    path('general/share_report', general.share_report, name='share_report'),
    path('general/answer_report', general.answer_report, name='answer_report'),

    ## utility to generate SQL for use in modifying 'report' columns
    path('general/gen_sql', general.gen_sql, name='gen_sql'),

    ## fix incorrectly set columns in this model
    path('general/fix_connector_report', general.fix_connector_report, name='fix_connector_report'),

    ## ==============================================================

    path('login_success', custom_admin.login_success, name='login_success'),

    path('admin/groups', custom_admin.manage_groups, name='manage_groups'),

    path('admin/echoes', custom_admin.manage_echoes, name='manage_echoes'),
    path('admin/echoes/<int:id>', custom_admin.edit_echo, name='edit_echo'),

    # path('admin/pdf_pages', custom_admin.pdf_pages, name='pdf_pages'),

    path('admin/pdf_pages/identifier/self', custom_admin.pdf_pages, name='pdf_pages_identifier_self'),
    path('admin/pdf_pages/identifier/voice', custom_admin.pdf_pages, name='pdf_pages_identifier_voice'),
    path('admin/pdf_pages/identifier/person', custom_admin.pdf_pages, name='pdf_pages_identifier_person'),
    path('admin/pdf_pages/identifier/place', custom_admin.pdf_pages, name='pdf_pages_identifier_place'),
    path('admin/pdf_pages/identifier/event', custom_admin.pdf_pages, name='pdf_pages_identifier_event'),
    path('admin/pdf_pages/identifier/object', custom_admin.pdf_pages, name='pdf_pages_identifier_object'),

    path('admin/pdf_pages/illuminator/self', custom_admin.pdf_pages, name='pdf_pages_illuminator_self'),
    path('admin/pdf_pages/illuminator/voice', custom_admin.pdf_pages, name='pdf_pages_illuminator_voice'),
    path('admin/pdf_pages/illuminator/person', custom_admin.pdf_pages, name='pdf_pages_illuminator_person'),
    path('admin/pdf_pages/illuminator/place', custom_admin.pdf_pages, name='pdf_pages_illuminator_place'),
    path('admin/pdf_pages/illuminator/event', custom_admin.pdf_pages, name='pdf_pages_illuminator_event'),
    path('admin/pdf_pages/illuminator/object', custom_admin.pdf_pages, name='pdf_pages_illuminator_object'),

    path('admin/pdf_pages/connector/group', custom_admin.pdf_pages, name='pdf_pages_connector_group'),
    path('admin/pdf_pages/connector/cadence', custom_admin.pdf_pages, name='pdf_pages_connector_cadence'),

    path('admin/pdf_pages/reflector/self|self', custom_admin.pdf_pages, name='pdf_pages_reflector_self_self'),
    path('admin/pdf_pages/reflector/self|person', custom_admin.pdf_pages, name='pdf_pages_reflector_self_person'),
    path('admin/pdf_pages/reflector/person|self', custom_admin.pdf_pages, name='pdf_pages_reflector_person_self'),
    path('admin/pdf_pages/reflector/person|person', custom_admin.pdf_pages, name='pdf_pages_reflector_person_person'),

    ## ==============================================================

    path('login', auth_views.LoginView.as_view(), name='login'),
    path('logout', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('password_reset', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<str:uidb64>/<str:token>', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # path('create-user', views.create_user, name='create_user'),
    path('self-words', identifier.self_words, name='self_words'),

    path('identifier/self', identifier.index, name='identifier_self'),
    path('identifier/voice', identifier.index, name='identifier_voice'),
    path('identifier/person', identifier.index, name='identifier_person'),
    path('identifier/place', identifier.index, name='identifier_place'),
    path('identifier/event', identifier.index, name='identifier_event'),
    path('identifier/object', identifier.index, name='identifier_object'),

    path('identifier/self/<int:id>', identifier.detail, name='identifier_self_detail'),
    path('identifier/voice/<int:id>', identifier.detail, name='identifier_voice_detail'),
    path('identifier/person/<int:id>', identifier.detail, name='identifier_person_detail'),
    path('identifier/place/<int:id>', identifier.detail, name='identifier_place_detail'),
    path('identifier/event/<int:id>', identifier.detail, name='identifier_event_detail'),
    path('identifier/object/<int:id>', identifier.detail, name='identifier_object_detail'),

    path('identifier/self/pdf/<int:id>', identifier.pdf, name='identifier_self_pdf'),
    path('identifier/voice/pdf/<int:id>', identifier.pdf, name='identifier_voice_pdf'),
    path('identifier/person/pdf/<int:id>', identifier.pdf, name='identifier_person_pdf'),
    path('identifier/place/pdf/<int:id>', identifier.pdf, name='identifier_place_pdf'),
    path('identifier/event/pdf/<int:id>', identifier.pdf, name='identifier_event_pdf'),
    path('identifier/object/pdf/<int:id>', identifier.pdf, name='identifier_object_pdf'),

    path('identifier/self/pdf-email/<int:id>', identifier.pdf_email, name='identifier_self_pdf_email'),
    path('identifier/voice/pdf-email/<int:id>', identifier.pdf_email, name='identifier_voice_pdf_email'),
    path('identifier/person/pdf-email/<int:id>', identifier.pdf_email, name='identifier_person_pdf_email'),
    path('identifier/place/pdf-email/<int:id>', identifier.pdf_email, name='identifier_place_pdf_email'),
    path('identifier/event/pdf-email/<int:id>', identifier.pdf_email, name='identifier_event_pdf_email'),
    path('identifier/object/pdf-email/<int:id>', identifier.pdf_email, name='identifier_object_pdf_email'),

    ## ==============================================================

    path('illuminator/self', illuminator.index, name='illuminator_self'),
    path('illuminator/voice', illuminator.index, name='illuminator_voice'),
    path('illuminator/person', illuminator.index, name='illuminator_person'),
    path('illuminator/place', illuminator.index, name='illuminator_place'),
    path('illuminator/event', illuminator.index, name='illuminator_event'),
    path('illuminator/object', illuminator.index, name='illuminator_object'),

    path('illuminator/self/<int:id>', illuminator.detail, name='illuminator_self_detail'),
    path('illuminator/voice/<int:id>', illuminator.detail, name='illuminator_voice_detail'),
    path('illuminator/person/<int:id>', illuminator.detail, name='illuminator_person_detail'),
    path('illuminator/place/<int:id>', illuminator.detail, name='illuminator_place_detail'),
    path('illuminator/event/<int:id>', illuminator.detail, name='illuminator_event_detail'),
    path('illuminator/object/<int:id>', illuminator.detail, name='illuminator_object_detail'),

    path('illuminator/self/pdf/<int:id>', illuminator.pdf, name='illuminator_self_pdf'),
    path('illuminator/voice/pdf/<int:id>', illuminator.pdf, name='illuminator_voice_pdf'),
    path('illuminator/person/pdf/<int:id>', illuminator.pdf, name='illuminator_person_pdf'),
    path('illuminator/place/pdf/<int:id>', illuminator.pdf, name='illuminator_place_pdf'),
    path('illuminator/event/pdf/<int:id>', illuminator.pdf, name='illuminator_event_pdf'),
    path('illuminator/object/pdf/<int:id>', illuminator.pdf, name='illuminator_object_pdf'),

    path('illuminator/self/pdf-email/<int:id>', illuminator.pdf_email, name='illuminator_self_pdf_email'),
    path('illuminator/voice/pdf-email/<int:id>', illuminator.pdf_email, name='illuminator_voice_pdf_email'),
    path('illuminator/person/pdf-email/<int:id>', illuminator.pdf_email, name='illuminator_person_pdf_email'),
    path('illuminator/place/pdf-email/<int:id>', illuminator.pdf_email, name='illuminator_place_pdf_email'),
    path('illuminator/event/pdf-email/<int:id>', illuminator.pdf_email, name='illuminator_event_pdf_email'),
    path('illuminator/object/pdf-email/<int:id>', illuminator.pdf_email, name='illuminator_object_pdf_email'),

    ## ==============================================================

    path('connector/index', connector.index, name='connector_index'),

    ## Handles POST when a cadence button is clicked in a connector (of type cadence) detail page
    path('connector/copy_connector', connector.copy_connector, name='copy_connector'),

    ## next 2 are Ajax endpoints
    path('connector/reports_by_group/<int:group_id>', connector.reports_by_group, name='reports_by_group'),
    path('connector/calculate_cadence_max', connector.calculate_cadence_max, name='calculate_cadence_max'),

    path('connector/pdf/<int:id>', connector.pdf, name='connector_pdf'),
    path('connector/pdf-email/<int:id>', connector.pdf_email, name='connector_pdf_email'),

    ## Better put this down here so the earlier paths get matched first
    path('connector/<int:id>', connector.detail, name='connector_detail'),

    ## ==============================================================

    path('reflector/index', reflector.index, name='reflector_index'),

    ## next 2 are Ajax endpoints
    path('reflector/reports_by_user/<int:user_id>', reflector.reports_by_user, name='reports_by_user'),

    path('reflector/pdf/<int:id>', reflector.pdf, name='reflector_pdf'),
    path('reflector/pdf-email/<int:id>', reflector.pdf_email, name='reflector_pdf_email'),

    ## Better put this down here so the earlier paths get matched first
    path('reflector/<int:id>', reflector.detail, name='reflector_detail'),

    ## ==============================================================

    path('echo/index', echo.index, name='echo_index'),

    path('echo/pdf/<int:id>', echo.pdf, name='echo_pdf'),

    path('echo/answer/<int:id>', echo.answer, name='echo_answer'),

    ## Better put this down here so the earlier paths get matched first
    path('echo/<int:id>', echo.detail, name='echo_detail'),

]
