from blog.models import BlogEntry
from config.settings import CACHE_ENABLED
from django.core.cache import cache


def get_blog_list():
    if CACHE_ENABLED:  # Проверяем включенность кеша
        key = f'blog_list'  # Создаем ключ для хранения
        blog_list = cache.get(key)  # Пытаемся получить данные
        if blog_list is None:
            # Если данные не были получены из кеша, то выбираем из БД и записываем в кеш
            blog_list = BlogEntry.objects.filter(
                is_published=True).order_by('-date_created')
            cache.set(key, blog_list)
    else:
        # Если кеш не был подключен, то просто обращаемся к БД
        blog_list = BlogEntry.objects.filter(
            is_published=True).order_by('-date_created')
    # Возвращаем результат
    return blog_list