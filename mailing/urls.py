"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.mailing, name='mailing')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='mailing')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path

import config
import mailing
from .views import (
    home,
    contact,
    ClientListView,
    ClientCreateView,
    ClientUpdateView,
    ClientDeleteView,
    MailingListView,
    MailingCreateView,
    MailingUpdateView,
    MailingDeleteView,
    MessageCreateView,
    MailingSendView,
    MailingDetailView, MessageDetailView, MessageDeleteView, MessageListView, MessageUpdateView, about,
)

app_name = 'mailing'

urlpatterns = [
    path('', home, name='home'),
    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),

    path('clients/', ClientListView.as_view(), name='client-list'),
    path('clients/create/', ClientCreateView.as_view(), name='client-create'),
    path('clients/<int:pk>/update/', ClientUpdateView.as_view(), name='client-update'),
    path('clients/<int:pk>/delete/', ClientDeleteView.as_view(), name='client-delete'),

    path('mailings/', MailingListView.as_view(), name='mailing_list'),
    path('mailings/create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailings/<int:pk>/update/', MailingUpdateView.as_view(), name='mailing-update'),
    path('mailings/<int:pk>/delete/', MailingDeleteView.as_view(), name='mailing-delete'),
    path('mailings/<int:pk>/send/', MailingSendView.as_view(), name='mailing-send'),
    path('mailings/<int:pk>/detail/', MailingDetailView.as_view(), name='mailing-detail'),

    path('message/', MessageListView.as_view(), name='message_list'),
    path('message/<int:pk>/detail/', MessageDetailView.as_view(), name='message-detail'),
    path('mailings/message/create/', MessageCreateView.as_view(), name='message-create'),
    path('message/<int:pk>/update/', MessageUpdateView.as_view(), name='message-update'),
    path('message/<int:pk>/delete/', MessageDeleteView.as_view(), name='message-delete'),


]

