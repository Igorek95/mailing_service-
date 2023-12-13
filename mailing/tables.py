import django_tables2 as tables
from mailing.models import Client, EmailFilling, EmailSubscribtion
from django.urls import reverse
from django.utils.html import format_html

from users.models import User


class UserTable(tables.Table):
    user_action = tables.Column(empty_values=(), verbose_name='Действия')

    class Meta:
        model = User
        template_name = "django_tables2/bootstrap5.html"
        fields = ("email", 'phone', 'is_active')
        attrs = {
            "class": "table table-striped table-dark table-hover table-sm",
            "style": "font-size: 18px; float: right; width: 80%; margin-top: 50px"
        }

    def render_email(self, value, record):
        return record.email

    def render_user_action(self, record):
        if record.is_active:
            return format_html('<a class="btn btn-danger" href="{}" role="button">Заблокировать</a>', reverse("mailing:block_user", args=(record.pk,)))
        else:
            return format_html('<a class="btn btn-warning" href="{}" role="button">Разблокировать</a>', reverse("mailing:unblock_user", args=(record.pk,)))


class ClientTable(tables.Table):
    class Meta:
        model = Client
        template_name = "django_tables2/bootstrap5.html"
        fields = ("email", 'full_name', 'comment')
        attrs = {
            "class": "table table-striped table-dark table-hover table-sm",
            "style": "font-size: 18px; float: right; width: 80%; margin-top: 50px"
        }

    def render_email(self, value, record):
        return format_html('<a href="{}" role="button">{}</a>', reverse("mailing:clients_detail", args=(record.pk,)), value)


class EmailFillingTable(tables.Table):
    class Meta:
        model = EmailFilling
        template_name = "django_tables2/bootstrap5.html"
        fields = ("email_template_name", 'email_subject', 'email_body')
        attrs = {
            "class": "table table-striped table-dark table-hover table-sm",
            "style": "font-size: 18px; float: right; width: 80%; margin-top: 50px"
        }

    def render_email_body(self, value, record):
        return f'{value[:50]}...'

    def render_email_template_name(self, value, record):
        return format_html('<a href="{}" role="button">{}</a>', reverse("mailing:templates_detail", args=(record.pk,)), value)


class EmailSubscribtionTable(tables.Table):
    class Meta:
        model = EmailSubscribtion
        template_name = "django_tables2/bootstrap5.html"
        fields = ('email_filling', 'periodic_time', 'time', 'status')
        attrs = {
            "class": "table table-striped table-dark table-hover table-sm",
            "style": "font-size: 18px; float: right; width: 80%; margin-top: 50px"
        }

    def render_email_filling(self, value, record):
        return format_html('<a href="{}" role="button">{}</a>', reverse("mailing:distributions_detail", args=(record.pk,)), value)
