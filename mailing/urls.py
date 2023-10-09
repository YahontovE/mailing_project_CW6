from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import ClientListView, home, ClientCreateView, ClientUpdateView, MailingListView, MailingCreateView, \
    MailingUpdateView, MailingDetailView, ClientDeleteView, MailingDeleteView

app_name = MailingConfig.name

urlpatterns = [
    path('', home, name='home'),
    path('client/', ClientListView.as_view(), name='client'),
    path('create_client/', ClientCreateView.as_view(), name='create_client'),
    path('edit_client/<int:pk>/', ClientUpdateView.as_view(), name='edit_client'),
    path('delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),

    path('mailing/', MailingListView.as_view(), name='mailing'),
    path('create_mail/', MailingCreateView.as_view(), name='create_mail'),
    path('edit_mail/<int:pk>/', MailingUpdateView.as_view(), name='edit_mail'),
    path('mail_detail/<int:pk>/', MailingDetailView.as_view(), name='mail_detail'),
    path('mailing_delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),
]
