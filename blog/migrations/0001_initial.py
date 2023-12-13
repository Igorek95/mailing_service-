# Generated by Django 4.2.6 on 2023-11-20 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlogEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry_title', models.CharField(max_length=150, verbose_name='заголовок')),
                ('entry_slug', models.CharField(max_length=150, verbose_name='slug')),
                ('entry_body', models.TextField(verbose_name='содержимое')),
                ('entry_img', models.ImageField(blank=True, null=True, upload_to='entry_img/', verbose_name='изображение')),
                ('date_created', models.DateField(auto_now_add=True, verbose_name='дата создания')),
                ('is_published', models.BooleanField(default=False, verbose_name='признак публикации')),
                ('views_count', models.IntegerField(default=0, verbose_name='количество просмотров')),
            ],
            options={
                'verbose_name': 'Топик',
                'verbose_name_plural': 'Топики',
            },
        ),
    ]
