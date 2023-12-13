from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User


NULLABLE = {'blank': True, 'null': True}


class BlogEntry(models.Model):
    entry_title = models.CharField(
        max_length=150, verbose_name='заголовок')
    entry_slug = models.CharField(
        max_length=150, verbose_name='slug')
    entry_body = models.TextField(verbose_name='содержимое')
    entry_img = models.ImageField(
        upload_to='entry_img/', verbose_name='изображение', **NULLABLE)
    date_created = models.DateField(
        verbose_name="дата создания", auto_now_add=True)
    is_published = models.BooleanField(
        verbose_name="признак публикации", default=False)
    views_count = models.IntegerField(
        verbose_name="количество просмотров", default=0)
    user = models.ForeignKey(User, verbose_name=_(
        "пользователь"), on_delete=models.CASCADE, default=None, **NULLABLE)

    def __str__(self):
        # Строковое отображение объекта
        return f'Название:{self.entry_title} Создание:{self.date_created} Опубликовано:{self.is_published} Просмотры:{self.views_count}'

    class Meta:
        verbose_name = 'Топик'  # Настройка для наименования одного объекта
        verbose_name_plural = 'Топики'  # Настройка для наименования набора объектов
