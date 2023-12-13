from django.contrib import admin
from mailing.models import Client, EmailFilling, EmailSubscribtion, EmailSubscribtionLogs

# Register your models here.


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'comment', 'user',)
    list_filter = ('user',)
    search_fields = ('email', 'full_name', 'comment', 'user')


@admin.register(EmailFilling)
class EmailFillingAdmin(admin.ModelAdmin):
    list_display = ('email_template_name', 'email_subject', 'user',)
    list_filter = ('user',)
    search_fields = ('email_template_name', 'email_subject', 'email_body',)


@admin.register(EmailSubscribtion)
class EmailSubscribtionAdmin(admin.ModelAdmin):
    list_display = ('periodic_time', 'email_filling',
                    'status', 'next_send_date', 'user')
    list_filter = ('periodic_time', 'status', 'user')
    search_fields = ('client', 'email_filling')


@admin.register(EmailSubscribtionLogs)
class EmailSubscribtionLogsAdmin(admin.ModelAdmin):
    list_display = ('subscription', 'last_try_date', 'is_success',
                    'last_mail_response')
    list_filter = ('is_success',)
    search_fields = ('subscription',)
