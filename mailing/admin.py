from django.contrib import admin

from mailing.models import Client, Mailing, MailingLog, Message


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'comment')
    search_fields = ('email', 'full_name', 'comment')
    list_filter = ('email', 'full_name', 'comment')


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('send_time', 'frequency', 'status')
    search_fields = ('send_time', 'frequency', 'status')
    list_filter = ('send_time', 'frequency', 'status')


@admin.register(MailingLog)
class MailingLogAdmin(admin.ModelAdmin):
    list_display = ('mailing', 'sent_time', 'status', 'server_response')
    search_fields = ('mailing', 'sent_time', 'status', 'server_response')
    list_filter = ('mailing', 'sent_time', 'status', 'server_response')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('mailing', 'subject', 'body')
    search_fields = ('mailing', 'subject', 'body')
    list_filter = ('mailing', 'subject', 'body')
