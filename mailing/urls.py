from django.urls import path
from mailing import views

app_name = 'mailing'

urlpatterns = [
    path('',  views.home, name='home'),
    path('contact/',  views.contact, name='contact'),
    path('about/', views.about, name='about'),

    path('manager_menu/', views.email_distribution_menu, name='email_distribution'),
    path('manager_rights/', views.ManagerTableView.as_view(), name='manager_menu'),
    path('manager_menu/block_user/<int:pk>',
         views.block_user, name='block_user'),
    path('manager_menu/unblock_user/<int:pk>',
         views.unblock_user, name='unblock_user'),

    path('clients', views.ClientTableView.as_view(), name='clients'),
    path('clients/create', views.ClientCreateView.as_view(), name='create_clients'),
    path('clients/<int:pk>/', views.ClientDetailView.as_view(), name='clients_detail'),
    path('clients/<int:pk>/update',
         views.ClientUpdateView.as_view(), name='update_clients'),
    path('clients/<int:pk>/delete',
         views.ClientDeleteView.as_view(), name='delete_clients'),

    path('mail_templates', views.EmailFillingTableView.as_view(),
         name='mail_templates'),
    path('mail_templates/create', views.EmailFillingCreateView.as_view(),
         name='create_templates'),
    path('mail_templates/<int:pk>',
         views.EmailFillingDetailView.as_view(), name='templates_detail'),
    path('mail_templates/<int:pk>/update',
         views.EmailFillingUpdateView.as_view(), name='update_templates'),
    path('mail_templates/<int:pk>/delete',
         views.EmailFillingDeleteView.as_view(), name='delete_templates'),

    path('mail_distributions', views.EmailSubscribtionTableView.as_view(),
         name='mail_distributions'),
    path('mail_distributions/create', views.EmailSubscribtionCreateView.as_view(),
         name='create_distributions'),
    path('mail_distributions/<int:pk>',
         views.EmailSubscribtionDetailView.as_view(), name='distributions_detail'),
    path('mail_distributions/<int:pk>/update',
         views.EmailSubscribtionUpdateView.as_view(), name='update_distributions'),
    path('mail_distributions/<int:pk>/delete',
         views.EmailSubscribtionDeleteView.as_view(), name='delete_distributions'),

]
