from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User


NULLABLE = {'blank': True, 'null': True}

PERIODIC_TIME_CHOICES = (('daily', 'Ежедневно'),
                        ('weekly', 'Еженедельно'),
                        ('monthly', 'Ежемесячно'),)
IS_ENABLED_CHOICES = (('enabled', 'Включить'),
                    ('disabled', 'Выключено'),)
STATUS_CHOICES = (('in_progress', 'В работе'),
                    ('idle', 'Ожидание'),)


class Client(models.Model):
    email = models.EmailField(verbose_name='email')
    full_name = models.CharField(verbose_name='ФИО', max_length=450)
    comment = models.TextField(verbose_name='Комментарий')
    user = models.ForeignKey(User, verbose_name=_("Создатель клиента"),
                             on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.email} {self.full_name}'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class EmailFilling(models.Model):
    email_template_name = models.CharField(
        verbose_name='темплейт', max_length=120)
    email_subject = models.CharField(
        verbose_name='тема письма', max_length=300)
    email_body = models.TextField(verbose_name='текст письма')
    user = models.ForeignKey(User, verbose_name=_("создатель темплейта"),
                             on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.email_template_name}'

    class Meta:
        verbose_name = 'наполнение письма'
        verbose_name_plural = 'наполнения писем'


class EmailSubscribtion(models.Model):
    time = models.TimeField(verbose_name='время рассылки')
    client = models.ManyToManyField(Client, verbose_name=_("клиент"))
    email_filling = models.ForeignKey(
        EmailFilling, verbose_name="наполнение письма", on_delete=models.CASCADE)
    periodic_time = models.CharField(
        verbose_name='периодичность', choices=PERIODIC_TIME_CHOICES, max_length=100)
    is_enabled = models.CharField(
        verbose_name='Включить рассылку', choices=IS_ENABLED_CHOICES, max_length=50)
    status = models.CharField(
        verbose_name='статус рассылки', default='idle', choices=STATUS_CHOICES, max_length=50)
    next_send_date = models.DateField(
        verbose_name='дата следующей отправки', auto_now_add=True, **NULLABLE)
    user = models.ForeignKey(User, verbose_name=_("создатель рассылки"),
                             on_delete=models.CASCADE)

    def __str__(self):
        return f'Клиент: {self.client}\nОбразец письма:\n{self.email_filling}\nПериодичность отправки:{self.periodic_time}'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'


class EmailSubscribtionLogs(models.Model):
    subscription = models.ForeignKey(
        EmailSubscribtion, verbose_name="рассылка", on_delete=models.CASCADE)
    last_try_date = models.DateTimeField(
        verbose_name="дата и время последней попытки", auto_now_add=True)
    is_success = models.BooleanField(
        verbose_name="успешно", default=True)
    last_mail_response = models.TextField(
        verbose_name="ответ почтового сервера", **NULLABLE)

    def __str__(self):
        return f'{self.subscription} {self.last_try_date} {self.is_success}'

    class Meta:
        verbose_name = 'лог рассылки'
        verbose_name_plural = 'логи рассылки'
