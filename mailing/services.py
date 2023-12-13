from datetime import datetime, timedelta
import logging
import smtplib
from django.core.mail import send_mail
from config import settings
from mailing.models import Client, EmailFilling, EmailSubscribtion, EmailSubscribtionLogs


class SendEmail:
    def __init__(self, client: Client, email_template: EmailFilling) -> None:
        self.client_email = client.email
        self.client_fullname = client.full_name

        self.email_subject = email_template.email_subject
        self.email_body = email_template.email_body

        self.email_subject = self.email_subject. \
            replace('@client_fullname', self.client_fullname). \
            replace('@client_email', self.client_email)
        self.email_body = self.email_body. \
            replace('@client_fullname', self.client_fullname). \
            replace('@client_email', self.client_email)

    def send_email(self):
        return send_mail(
            self.email_subject,
            self.email_body,
            settings.EMAIL_HOST_USER,
            [self.client_email],
            fail_silently=False
        )


def start_distribution_task():
    list_of_distributions = EmailSubscribtion.objects.filter(
        is_enabled='enabled',  # Рассылка включена
        status='idle',  # Не в работе
        # Дата следующей отправки меньше текущей даты
        next_send_date__lte=datetime.now(),
        time__lte=datetime.now().time()  # Время отправки меньше текущего времени
    )

    sending_errors = ''
    for distribution in list_of_distributions:
        distribution.status = 'in_progress'
        distribution.save()

        for client in distribution.client.all():
            try:
                sending_result = SendEmail(client, distribution.email_filling).send_email()
            except smtplib.SMTPException as e:
                sending_errors += f'Send for {client.email} failed. Message: {str(e.message)}; '

            if sending_result:
                match distribution.periodic_time:
                    case 'daily':
                        delta = timedelta(1)
                    case 'weekly':
                        delta = timedelta(7)
                    case 'monthly':
                        delta = timedelta(30)
                distribution.next_send_date = datetime.now() + delta

        log = EmailSubscribtionLogs()
        log.subscription = distribution
        log.last_try_date = datetime.now()
        log.is_success = bool(sending_result)
        if sending_errors:
            log.last_mail_response = sending_errors
        else:
            log.last_mail_response = 'success'
        log.save()

        distribution.status = 'idle'
        distribution.save()