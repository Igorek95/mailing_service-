from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import User

NULLABLE = {'null': True, 'blank': True}


class Client(models.Model):
    email = models.EmailField(unique=True, verbose_name='Email')
    full_name = models.CharField(max_length=100, verbose_name='ФИО')
    comment = models.TextField(verbose_name='Комментарий')
    user = models.ForeignKey(User, verbose_name=_(
        "пользователь"), on_delete=models.CASCADE, default=None, **NULLABLE)

    def __str__(self):
        return f'{self.full_name} ({self.email})'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Mailing(models.Model):
    STATUS_CHOICES = [
        ('Создана', 'Создана'),
        ('Запущена', 'Запущена'),
        ('Завершена', 'Завершена'),
    ]
    FREQUENCY_CHOICES = [
        ('Раз в день', 'Раз в день'),
        ('Раз в неделю', 'Раз в неделю'),
        ('Раз в месяц', 'Раз в месяц'),
    ]
    send_time = models.DateTimeField(verbose_name='Время отправки', )
    frequency = models.CharField(max_length=50, choices=FREQUENCY_CHOICES, verbose_name='частота отправки', )
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Создана', verbose_name='Статус отправки')
    user = models.ForeignKey(User, verbose_name=_(
        "пользователь"), on_delete=models.CASCADE, default=None, **NULLABLE)

    def __str__(self):
        return f'{self.send_time} ({self.frequency} {self.status})'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class Message(models.Model):
    subject = models.CharField(max_length=255, verbose_name='Тема')
    body = models.TextField(verbose_name='Текст')
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE,
                                verbose_name='Переодичность рассылки')

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class MailingLog(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Отправитель')
    sent_time = models.DateTimeField(verbose_name='Время отправления')
    status = models.CharField(max_length=20, default='created', verbose_name='Статус отправления')
    server_response = models.TextField(verbose_name='Ответ от сервера')

    def __str__(self):
        return f'{self.mailing} ({self.sent_time} {self.status})'

    class Meta:
        verbose_name = 'Журнал отправки'
        verbose_name_plural = 'Журнал отправки'
